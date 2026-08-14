# -*- coding: utf-8 -*-
import sys
import io
import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

user_home = Path(os.path.expanduser("~"))
chrome_profile_dir = user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data"

out_dir = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\scratch\diagnostico_chrome_native")
out_dir.mkdir(parents=True, exist_ok=True)

plataformas = {
    "tiendanube": "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new",
    "payhip": "https://payhip.com/product/add/digital",
    "gumroad": "https://gumroad.com/products/new",
    "hotmart": "https://app.hotmart.com/tools/products/create",
    "amazon_kdp": "https://kdp.amazon.com/en_US/title-setup/kindle/new"
}

async def diagnosticar_chrome_native():
    print(f"Verificando inicio de sesion directo usando el perfil nativo de Chrome ({chrome_profile_dir})...\n")
    async with async_playwright() as p:
        try:
            # Launch context pointing directly to user's standard Chrome profile
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(chrome_profile_dir),
                headless=True,
                channel="chrome"
            )
            page = context.pages[0] if context.pages else await context.new_page()
            
            for name, url in plataformas.items():
                print(f"[*] Verificando {name.upper()} ({url})...")
                try:
                    response = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    title = await page.title()
                    current_url = page.url
                    shot_path = out_dir / f"{name}_native_status.png"
                    await page.screenshot(path=str(shot_path))
                    
                    print(f"    URL Actual: {current_url}")
                    print(f"    Título Página: {title}")
                    print(f"    Screenshot: {shot_path}\n")
                except Exception as e:
                    print(f"    [Aviso] {name}: {e}\n")
                    
            await context.close()
        except Exception as e:
            print(f"Error al conectar con Chrome nativo (posiblemente Chrome este abierto): {e}")

if __name__ == "__main__":
    asyncio.run(diagnosticar_chrome_native())
