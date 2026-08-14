# -*- coding: utf-8 -*-
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if 'hotmart' in pg.url][0]
        
        await hotmart_page.goto('https://app.hotmart.com/products', wait_until='networkidle')
        await hotmart_page.wait_for_timeout(3000)

        js = """
        () => {
            const items = Array.from(document.querySelectorAll('a, button, div')).map(e => ({
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : '',
                href: e.href || ''
            }));
            return items.filter(x => x.href.includes('/products/'));
        }
        """
        js_clean = """
        () => {
            return Array.from(document.querySelectorAll('a[href*="/products/"]')).map(e => ({
                titulo: e.innerText ? e.innerText.trim() : '',
                url: e.href
            }));
        }
        """
        prods = await hotmart_page.evaluate(js_clean)
        print("PRODUCTOS OBTENIDOS EN HOTMART:")
        for pr in prods:
            print("  •", pr['titulo'], "->", pr['url'])

if __name__ == "__main__":
    asyncio.run(main())
