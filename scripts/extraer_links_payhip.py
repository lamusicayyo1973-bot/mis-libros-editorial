# -*- coding: utf-8 -*-
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()
        
        await page.goto("https://payhip.com/products", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        js = """
        () => {
            const links = Array.from(document.querySelectorAll('a')).map(e => ({
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : '',
                href: e.href || ''
            }));
            return links.filter(x => x.href.includes('/b/') || x.href.includes('payhip.com/b/'));
        }
        """
        data = await page.evaluate(js)
        print("ENLACES DIRECTOS EN PAYHIP:")
        for item in data:
            print(f"  • {item['text']} -> {item['href']}")

        await page.close()

if __name__ == "__main__":
    asyncio.run(main())
