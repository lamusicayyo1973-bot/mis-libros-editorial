# -*- coding: utf-8 -*-
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        urls = [
            "https://payhip.com/b/JgoYS",
            "https://payhip.com/b/YpJPq",
            "https://payhip.com/b/rIbUa",
            "https://payhip.com/b/pbrym",
            "https://payhip.com/b/zFLvQ",
            "https://payhip.com/b/Sj0F1"
        ]
        
        print("VERIFICANDO ENLACES PÚBLICOS EN PAYHIP:")
        for url in urls:
            try:
                res = await page.goto(url, wait_until="networkidle")
                title = await page.title()
                print(f"  • Status {res.status}: '{title}' -> {url}")
            except Exception as e:
                print(f"  • Error en {url}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
