# -*- coding: utf-8 -*-
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        await hotmart_page.goto("https://app.hotmart.com/products/manage/8258977/info", wait_until="networkidle")
        await hotmart_page.wait_for_timeout(3000)

        js = """
        () => {
            const links = Array.from(document.querySelectorAll('a')).map(a => ({
                text: a.innerText ? a.innerText.trim().replace(/\\n+/g, ' ') : '',
                href: a.href || ''
            })).filter(x => x.href.includes('/manage/'));
            return links;
        }
        """
        menu = await hotmart_page.evaluate(js)
        print("MENU DE GESTION DE PRODUCTO EN HOTMART:")
        seen = set()
        for item in menu:
            t = item['text']
            u = item['href']
            if u not in seen:
                seen.add(u)
                print(f"  • {t} -> {u}")

if __name__ == "__main__":
    asyncio.run(main())
