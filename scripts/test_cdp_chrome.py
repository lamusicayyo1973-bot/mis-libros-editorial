# -*- coding: utf-8 -*-
import sys
import io
import asyncio
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def connect_chrome_cdp():
    print("Testing connection to open Chrome via CDP (port 9222)...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected to active Chrome browser session!")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            
            urls = {
                "Gumroad": "https://gumroad.com/dashboard",
                "Hotmart": "https://app.hotmart.com/home",
                "Amazon KDP": "https://kdp.amazon.com/bookshelf"
            }
            
            for name, url in urls.items():
                print(f"Checking {name} in active Chrome session...")
                new_page = await context.new_page()
                await new_page.goto(url, timeout=15000)
                print(f"  [{name}] URL: {new_page.url} | Title: {await new_page.title()}")
                
            await browser.close()
        except Exception as e:
            print("CDP Error (Chrome not started with debugging port):", e)

if __name__ == "__main__":
    asyncio.run(connect_chrome_cdp())
