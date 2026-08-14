# -*- coding: utf-8 -*-
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()

        print("Navegando a https://app.hotmart.com/products/add...")
        await page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        print("URL RESULTADO:", page.url)

        # Sacar captura de pantalla
        shot_path = r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_crear_nuevo.png"
        await page.screenshot(path=shot_path, full_page=True)
        print("Captura guardada en:", shot_path)

        await page.close()

if __name__ == "__main__":
    asyncio.run(main())
