# -*- coding: utf-8 -*-
import sys
import io
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Paths for user data
edge_user_data = Path(r"C:\Users\nicol\AppData\Local\Microsoft\Edge\User Data")
chrome_user_data = Path(r"C:\Users\nicol\AppData\Local\Google\Chrome\User Data")

async def test_session():
    user_data_path = str(chrome_user_data if chrome_user_data.exists() else edge_user_data)
    channel = "chrome" if chrome_user_data.exists() else "msedge"
    
    print(f"Using persistent browser context: {user_data_path} ({channel})")
    
    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_path,
                channel=channel,
                headless=True,
                args=["--remote-debugging-port=9222"]
            )
            page = context.pages[0] if context.pages else await context.new_page()
            
            urls = {
                "tiendanube": "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new",
                "payhip": "https://payhip.com/product/add/digital",
                "gumroad": "https://gumroad.com/dashboard",
                "hotmart": "https://app.hotmart.com/home",
                "amazon_kdp": "https://kdp.amazon.com/bookshelf"
            }
            
            for name, url in urls.items():
                print(f"Checking {name} with saved user cookies...")
                await page.goto(url, timeout=15000)
                print(f"  [{name}] URL Actual: {page.url} | Title: {await page.title()}")
                
            await context.close()
        except Exception as e:
            print("Error testing persistent context:", e)

if __name__ == "__main__":
    asyncio.run(test_session())
