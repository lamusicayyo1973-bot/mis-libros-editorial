# -*- coding: utf-8 -*-
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            print("Navegando a https://payhip.com/products en Brave...")
            await page.goto("https://payhip.com/products", wait_until="networkidle")
            await page.wait_for_timeout(3000)

            js = """
            () => {
                const rows = Array.from(document.querySelectorAll('tr, .js-product-row')).map(e => {
                    const titleEl = e.querySelector('.product-title, a[href*="/b/"], a');
                    const linkEl = e.querySelector('a[href*="/b/"]');
                    return {
                        title: titleEl ? titleEl.innerText.trim() : '',
                        link: linkEl ? linkEl.href : ''
                    };
                });
                return rows.filter(x => x.title.length > 0);
            }
            """
            products = await page.evaluate(js)
            print("PRODUCTOS EN PAYHIP:")
            for p_item in products:
                print(f"  • {p_item['title']} -> {p_item['link']}")

            await page.close()
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
