# -*- coding: utf-8 -*-
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        print("Navegando a precificación en Hotmart...")
        await hotmart_page.goto("https://app.hotmart.com/products/add/4/prices", wait_until="networkidle")
        await hotmart_page.wait_for_timeout(2500)
        print("URL actual precificación:", hotmart_page.url)

        js_inputs = """
        () => {
            return Array.from(document.querySelectorAll('input, select, textarea, button')).map(e => ({
                tag: e.tagName,
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                placeholder: e.placeholder || '',
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : ''
            }));
        }
        """
        inputs = await hotmart_page.evaluate(js_inputs)
        print("\nCAMPOS EN PRECIFICACION:")
        for inp in inputs:
            if inp['id'] or inp['name'] or inp['placeholder'] or 'Guardar' in inp['text'] or 'Continuar' in inp['text']:
                print("  •", inp)

if __name__ == "__main__":
    asyncio.run(main())
