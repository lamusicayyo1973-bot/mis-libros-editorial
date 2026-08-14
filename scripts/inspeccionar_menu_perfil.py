# -*- coding: utf-8 -*-
"""
INSPECCIONAR PESTAÑAS DE MI CUENTA EN HOTMART
"""
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        js = """
        () => {
            const tabs = Array.from(document.querySelectorAll('a, button, li, [role="tab"]')).map(e => ({
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : '',
                href: e.href || e.getAttribute('href') || ''
            }));
            return tabs.filter(x => x.text.length > 2);
        }
        """
        elements = await page.evaluate(js)
        print("PESTAÑAS Y MENÚS DISPONIBLES EN PANTALLA:")
        for el in elements:
            if any(w in el['text'].lower() for w in ['perfil', 'datos', 'cuenta', 'personales', 'información', 'financiero', 'documento']):
                print(f"  • {el['text']} -> {el['href']}")

if __name__ == "__main__":
    asyncio.run(main())
