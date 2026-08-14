# -*- coding: utf-8 -*-
import sys
import os
import io
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

book_folder = Path(r"C:\Proyectos\mis-libros-editorial\libros\el-algoritmo-personal")
ficha_file = book_folder / "ficha_producto.json"
with open(ficha_file, "r", encoding="utf-8") as f:
    ficha = json.load(f)

titulo = f"{ficha.get('titulo')}: {ficha.get('subtitulo')}"
descripcion = f"{ficha.get('copy_ventas', {}).get('headline')}\n\n{ficha.get('copy_ventas', {}).get('cuerpo')}"
precio_usd = "20.00"

portada_file = book_folder / "portada.jpg"
docx_file = book_folder / "libro.docx"

async def main():
    print("================================================================")
    print("🚀 PUBLICANDO EN VIVO EN PAYHIP USANDO NAVEGADOR LOGUEADO")
    print("================================================================")
    
    async with async_playwright() as p:
        # Launch persistent context channel chrome visible
        user_home = Path(os.path.expanduser("~"))
        chrome_user_data = user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data"
        
        # Connect via CDP if running or launch chrome visible
        browser = None
        try:
            print("Intentando conexión CDP con puerto 9222...")
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            print("  [✓] Conectado a Chrome activo!")
        except Exception:
            print("Lanzando ventana visible de Chrome...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(Path(r"C:\Proyectos\loki\automation\loki_session_profile")),
                headless=False,
                channel="chrome",
                args=["--start-maximized"]
            )
            page = context.pages[0] if context.pages else await context.new_page()

        print("\n[+] Navegando a Payhip (Cargar Producto Digital)...")
        await page.goto("https://payhip.com/product/add/digital", wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Check if redirected to login
        if "login" in page.url:
            print("  [!] Payhip requiere inicio de sesión. Por favor inicia sesión en la ventana de Chrome.")
            print("  Esperando 15 segundos para inicio de sesión...")
            await asyncio.sleep(15)
            await page.goto("https://payhip.com/product/add/digital", wait_until="domcontentloaded")
            await asyncio.sleep(3)

        # Fill Title
        t_in = page.locator('input[name="title"], input#product-title')
        if await t_in.count() > 0:
            await t_in.first.fill(titulo)
            print("  [✓] Título cargado")

        # Fill Price
        p_in = page.locator('input[name="price"], input#product-price')
        if await p_in.count() > 0:
            await p_in.first.fill(precio_usd)
            print("  [✓] Precio cargado ($20.00)")

        # Upload .docx file
        if docx_file.exists():
            f_in = page.locator('input[type="file"][name="file"], input#digital-file')
            if await f_in.count() > 0:
                await f_in.first.set_input_files(str(docx_file))
                print(f"  [✓] Manuscrito .docx adjuntado: {docx_file.name}")
                await asyncio.sleep(3)

        # Upload cover image
        if portada_file.exists():
            img_in = page.locator('input[type="file"][name="cover"], input#product-cover')
            if await img_in.count() > 0:
                await img_in.first.set_input_files(str(portada_file))
                print(f"  [✓] Portada adjuntada: {portada_file.name}")
                await asyncio.sleep(3)

        # Click Add Product
        add_btn = page.locator('button[type="submit"], input[type="submit"], button:has-text("Add Product")')
        if await add_btn.count() > 0:
            print("  [✓] Presionando botón 'Add Product'...")
            await add_btn.first.click()
            await asyncio.sleep(5)
            print(f"  [✓] URL resultado: {page.url}")

        print("\n================================================================")
        print("🎉 ¡PROCESO DE CARGA DE PAYHIP FINALIZADO!")
        print("================================================================")
        await asyncio.sleep(3)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
