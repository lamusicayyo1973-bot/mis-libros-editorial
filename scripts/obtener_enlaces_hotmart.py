# -*- coding: utf-8 -*-
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()

        print("Navegando al Panel de Productos de Hotmart...")
        await page.goto("https://app.hotmart.com/products", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Clic en pestañas si existen
        tab = await page.query_selector('text="Soy Productor(a)"')
        if tab:
            await tab.click()
            await page.wait_for_timeout(2000)

        # Tomar captura de pantalla de verificación
        screenshot_path = r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_productos_lista.png"
        await page.screenshot(path=screenshot_path)
        print(f"Captura guardada en: {screenshot_path}")

        # Extraer enlaces
        links = await page.query_selector_all('a[href*="products"]')
        print("\nENLACES ENCONTRADOS EN HOTMART:")
        for link in links:
            href = await link.get_attribute("href")
            text = await link.inner_text()
            text_clean = text.strip().replace('\n', ' ')
            if href and ("manage" in href or "info" in href or "details" in href):
                print(f"  • {text_clean}: https://app.hotmart.com{href if href.startswith('/') else '/' + href}")

        await page.close()

if __name__ == "__main__":
    asyncio.run(main())
