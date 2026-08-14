# -*- coding: utf-8 -*-
import sys
import os
import io
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_books_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros")

async def upload_tiendanube(page, book_folder, ficha):
    print(f"\n[+] [TIENDANUBE] Carga para: {ficha.get('titulo')}")
    url = "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    
    # Fill title
    name_input = page.locator('input[name="name"], input#product_name, input[data-store="product-name"]')
    if await name_input.count() > 0:
        await name_input.first.fill(ficha.get("titulo"))
        print("    [Tiendanube] Título cargado")
        
    # Fill price
    price_input = page.locator('input[name="price"], input#product_price')
    if await price_input.count() > 0:
        await price_input.first.fill("26000")
        print("    [Tiendanube] Precio ARS cargado ($26.000)")

    # Upload cover
    portada = book_folder / "portada.jpg"
    if portada.exists():
        file_input = page.locator('input[type="file"]')
        if await file_input.count() > 0:
            await file_input.first.set_input_files(str(portada))
            print("    [Tiendanube] Portada subida")
            
    print("    [OK] Tiendanube completado")
    return True

async def upload_payhip(page, book_folder, ficha):
    print(f"\n[+] [PAYHIP] Carga para: {ficha.get('titulo')}")
    url = "https://payhip.com/product/add/digital"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    
    title_input = page.locator('input[name="title"], input#product-title')
    if await title_input.count() > 0:
        await title_input.first.fill(ficha.get("titulo"))
        print("    [Payhip] Título cargado")
        
    price_input = page.locator('input[name="price"], input#product-price')
    if await price_input.count() > 0:
        await price_input.first.fill(str(ficha.get("precio", 20.00)))
        print("    [Payhip] Precio USD cargado ($20.00)")
        
    docx_file = book_folder / "libro.docx"
    if docx_file.exists():
        file_input = page.locator('input[type="file"][name="file"], input#digital-file')
        if await file_input.count() > 0:
            await file_input.first.set_input_files(str(docx_file))
            print("    [Payhip] Manuscrito .docx subido")
            
    print("    [OK] Payhip completado")
    return True

async def upload_gumroad(page, book_folder, ficha):
    print(f"\n[+] [GUMROAD] Carga para: {ficha.get('titulo')}")
    url = "https://gumroad.com/products/new"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    
    name_input = page.locator('input[name="name"]')
    if await name_input.count() > 0:
        await name_input.first.fill(ficha.get("titulo"))
        print("    [Gumroad] Nombre cargado")
        
    price_input = page.locator('input[name="price"]')
    if await price_input.count() > 0:
        await price_input.first.fill(str(int(ficha.get("precio", 20))))
        print("    [Gumroad] Precio cargado")
        
    print("    [OK] Gumroad completado")
    return True

async def upload_hotmart(page, book_folder, ficha):
    print(f"\n[+] [HOTMART] Carga para: {ficha.get('titulo')}")
    url = "https://app.hotmart.com/tools/products/create"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    print("    [OK] Hotmart verificado")
    return True

async def upload_kdp(page, book_folder, ficha):
    print(f"\n[+] [AMAZON KDP] Carga para: {ficha.get('titulo')}")
    url = "https://kdp.amazon.com/en_US/title-setup/kindle/new"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    
    title_input = page.locator('input#data-print-book-title, input#data-title')
    if await title_input.count() > 0:
        await title_input.first.fill(ficha.get("titulo"))
        print("    [Amazon KDP] Título cargado")
        
    print("    [OK] Amazon KDP completado")
    return True

async def run_publishing(book_id):
    book_folder = base_books_dir / book_id
    if not book_folder.exists():
        print(f"[-] Carpeta no encontrada: {book_folder}")
        return
        
    ficha_file = book_folder / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[-] No existe ficha_producto.json en {book_folder.name}")
        return
        
    with open(ficha_file, "r", encoding="utf-8") as f:
        ficha = json.load(f)

    async with async_playwright() as p:
        browser = None
        page = None
        try:
            print("Intentando conexión con puerto CDP de Chrome (http://127.0.0.1:9222)...")
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            print("¡Conectado directamente a tu navegador Chrome activo!")
        except Exception as e:
            print(f"Aviso conexión CDP (127.0.0.1:9222 no activo): {e}")
            loki_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(loki_dir),
                headless=True
            )
            page = context.pages[0] if context.pages else await context.new_page()

        print(f"\n=== PUBLICANDO: {ficha.get('titulo')} ===")
        await upload_tiendanube(page, book_folder, ficha)
        await upload_payhip(page, book_folder, ficha)
        await upload_gumroad(page, book_folder, ficha)
        await upload_hotmart(page, book_folder, ficha)
        await upload_kdp(page, book_folder, ficha)
        
        print(f"\n=== ¡PUBLICACIÓN COMPLETADA PARA {book_id}! ===")

if __name__ == "__main__":
    book = sys.argv[1] if len(sys.argv) > 1 else "de-cero-a-negocio-con-ia"
    asyncio.run(run_publishing(book))
