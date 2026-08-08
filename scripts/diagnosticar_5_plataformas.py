# -*- coding: utf-8 -*-
import sys
import io
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

out_dir = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\scratch\diagnostico")
out_dir.mkdir(parents=True, exist_ok=True)

plataformas = {
    "tiendanube": "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new",
    "payhip": "https://payhip.com/product/add/digital",
    "gumroad": "https://gumroad.com/products/new",
    "hotmart": "https://app.hotmart.com/tools/products/create",
    "amazon_kdp": "https://kdp.amazon.com/en_US/title-setup/kindle/new"
}

loki_profile_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")

async def diagnosticar():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(loki_profile_dir),
            headless=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("Diagnosticando las 5 plataformas de venta con perfil persistente...\n")
        
        for name, url in plataformas.items():
            print(f"[*] Verificando {name.upper()} ({url})...")
            try:
                response = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                title = await page.title()
                current_url = page.url
                status = response.status if response else "N/A"
                shot_path = out_dir / f"{name}_status.png"
                await page.screenshot(path=str(shot_path))
                
                print(f"    Status: {status}")
                print(f"    URL Actual: {current_url}")
                print(f"    Título Página: {title}")
                print(f"    Screenshot guardada: {shot_path}\n")
            except Exception as e:
                print(f"    [ERROR] Falló al cargar {name}: {e}\n")
                
        await context.close()

if __name__ == "__main__":
    asyncio.run(diagnosticar())
