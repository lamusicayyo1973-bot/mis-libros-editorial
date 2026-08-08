# -*- coding: utf-8 -*-
import sys
import io
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

loki_profile_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")
loki_profile_dir.mkdir(parents=True, exist_ok=True)

async def setup_loki_browser():
    print(f"Opening Loki dedicated automated browser context in {loki_profile_dir}...")
    async with async_playwright() as p:
        # Launch persistent context with dedicated profile directory
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(loki_profile_dir),
            headless=False, # Open visible browser window so user can login once if needed
            args=["--start-maximized"]
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        urls = [
            ("Tiendanube", "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new"),
            ("Payhip", "https://payhip.com/product/add/digital"),
            ("Gumroad", "https://gumroad.com/products/new"),
            ("Hotmart", "https://app.hotmart.com/tools/products/create"),
            ("Amazon KDP", "https://kdp.amazon.com/")
        ]
        
        print("\nOpening all 5 platforms in dedicated Loki browser context...")
        for name, url in urls:
            print(f"  [+] Opening {name}: {url}")
            new_page = await context.new_page()
            await new_page.goto(url)
            
        print("\nAll 5 platforms opened in dedicated browser profile!")
        print("Please check which platforms need login, log in once, and close the browser.")

if __name__ == "__main__":
    asyncio.run(setup_loki_browser())
