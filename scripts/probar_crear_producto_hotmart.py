# -*- coding: utf-8 -*-
"""
===============================================================================
VERIFICAR SI LA CUENTA DE HOTMART PUEDE CREAR PRODUCTOS DIRECTAMENTE
===============================================================================
Comprueba si https://app.hotmart.com/products/add está totalmente accesible.
===============================================================================
"""

import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = [pg for pg in context.pages if "hotmart" in pg.url][0]

            print("Probando acceso a https://app.hotmart.com/products/add...")
            await page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
            await page.wait_for_timeout(3000)

            print("URL actual:", page.url)

            # Sacar captura
            shot_path = r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_acceso_crear.png"
            await page.screenshot(path=shot_path, full_page=True)
            print(f"Captura guardada en: {shot_path}")

        except Exception as e:
            print("Error probando acceso:", e)

if __name__ == "__main__":
    asyncio.run(main())
