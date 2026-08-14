# -*- coding: utf-8 -*-
"""
===============================================================================
LISTAR Y VERIFICAR TODOS LOS PRODUCTOS PUBLICADOS EN HOTMART
===============================================================================
Obtiene la lista completa de productos desde la vista de Hotmart
y genera los enlaces directos de administración de los 15 libros.
===============================================================================
"""

import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()

        print("Navegando a https://app.hotmart.com/products...")
        await page.goto("https://app.hotmart.com/products", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Clic en tab Productor si está disponible
        producer_tab = await page.query_selector('text="Soy Productor(a)"')
        if producer_tab:
            await producer_tab.click()
            await page.wait_for_timeout(2000)

        # Capturar la lista completa en la pantalla
        screenshot_path = r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_productos_lista.png"
        await page.screenshot(path=screenshot_path, full_page=True)

        js = """
        () => {
            const items = Array.from(document.querySelectorAll('tr, .hot-table-row, [class*="product-card"], a')).map(e => ({
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : '',
                href: e.href || e.getAttribute('href') || ''
            }));
            return items.filter(x => x.text.length > 5);
        }
        """
        data = await page.evaluate(js)
        print("\nPRODUCTOS DETECTADOS EN PANEL HOTMART:")
        for item in data[:30]:
            print(f"  • {item['text']} -> {item['href']}")

        await page.close()

if __name__ == "__main__":
    asyncio.run(main())
