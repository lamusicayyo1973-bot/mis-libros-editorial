# -*- coding: utf-8 -*-
import sys
import io
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

urls = {
    "tiendanube": "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new",
    "payhip": "https://payhip.com/product/add/digital",
    "gumroad": "https://gumroad.com/products/new",
    "hotmart": "https://app.hotmart.com/tools/products/create",
    "amazon_kdp": "https://kdp.amazon.com/en_US/title-setup/kindle/new"
}

async def test_cdp():
    print("Conectando con Chrome abierto via Remote Debugging CDP (port 9222)...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("  [OK] Conectado exitosamente con tu navegador Chrome activo!")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            
            for name, url in urls.items():
                print(f"[*] Verificando {name.upper()}...")
                await page.goto(url, wait_until="domcontentloaded")
                print(f"    URL: {page.url}")
                print(f"    Título: {await page.title()}\n")
                
        except Exception as e:
            print(f"  [Aviso] CDP no detectado (Chrome no esta corriendo con port 9222): {e}")

if __name__ == "__main__":
    asyncio.run(test_cdp())
