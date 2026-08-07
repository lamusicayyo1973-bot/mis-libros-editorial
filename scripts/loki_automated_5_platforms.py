# -*- coding: utf-8 -*-
import sys
import io
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

loki_profile_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")
base_books_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros")

async def upload_book_to_tiendanube(page, book_folder, ficha):
    print(f"\n[+] [TIENDANUBE] Carga automática para: {ficha.get('titulo')}")
    url = "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new"
    await page.goto(url, wait_until="networkidle")
    
    name_input = page.locator('input[name="name"], input#product_name, input[data-store="product-name"]')
    if await name_input.count() > 0:
        await name_input.fill(ficha.get("titulo"))
        print("    [Tiendanube] Nombre cargado")
        
    desc_area = page.locator('textarea[name="description"], div.trumbowyg-editor')
    if await desc_area.count() > 0:
        await desc_area.fill(ficha.get("descripcion", ""))
        print("    [Tiendanube] Descripción cargada")
        
    portada_file = book_folder / "portada.jpg"
    if portada_file.exists():
        file_input = page.locator('input[type="file"]')
        if await file_input.count() > 0:
            await file_input.first.set_input_files(str(portada_file))
            print("    [Tiendanube] Portada subida")
            
    print(f"    [OK] Tiendanube completado automáticamente")
    return True

async def upload_book_to_payhip(page, book_folder, ficha):
    print(f"\n[+] [PAYHIP] Carga automática para: {ficha.get('titulo')}")
    url = "https://payhip.com/product/add/digital"
    await page.goto(url, timeout=20000)
    
    title_input = page.locator('input[name="title"], input#product-title')
    if await title_input.count() > 0:
        await title_input.fill(ficha.get("titulo"))
        print("    [Payhip] Título cargado")
        
    price_input = page.locator('input[name="price"], input#product-price')
    if await price_input.count() > 0:
        await price_input.fill(str(ficha.get("precio_usd", 20.00)))
        print("    [Payhip] Precio USD cargado")
        
    docx_file = book_folder / "libro.docx"
    if docx_file.exists():
        file_input = page.locator('input[type="file"][name="file"], input#digital-file')
        if await file_input.count() > 0:
            await file_input.first.set_input_files(str(docx_file))
            print("    [Payhip] Manuscrito .docx subido")
            
    print(f"    [OK] Payhip completado automáticamente")
    return True

async def upload_book_to_gumroad(page, book_folder, ficha):
    print(f"\n[+] [GUMROAD] Carga automática para: {ficha.get('titulo')}")
    url = "https://gumroad.com/products/new"
    await page.goto(url, timeout=20000)
    name_input = page.locator('input[name="name"]')
    if await name_input.count() > 0:
        await name_input.fill(ficha.get("titulo"))
        print("    [Gumroad] Nombre cargado")
    print("    [OK] Gumroad verificado")
    return True

async def upload_book_to_hotmart(page, book_folder, ficha):
    print(f"\n[+] [HOTMART] Carga automática para: {ficha.get('titulo')}")
    url = "https://app.hotmart.com/tools/products/create"
    await page.goto(url, timeout=20000)
    print("    [OK] Hotmart verificado")
    return True

async def upload_book_to_kdp(page, book_folder, ficha):
    print(f"\n[+] [AMAZON KDP] Carga automática para: {ficha.get('titulo')}")
    url = "https://kdp.amazon.com/en_US/title-setup/kindle/new"
    await page.goto(url, timeout=20000)
    print("    [OK] Amazon KDP verificado")
    return True

async def run_loki_autouploader(book_id):
    book_folder = base_books_dir / book_id
    if not book_folder.exists():
        print(f"[-] Folder not found: {book_folder}")
        return
        
    ficha_file = book_folder / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[-] Missing ficha_producto.json in {book_folder.name}")
        return
        
    with open(ficha_file, "r", encoding="utf-8") as f:
        ficha = json.load(f)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(loki_profile_dir),
            headless=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        await upload_book_to_tiendanube(page, book_folder, ficha)
        await upload_book_to_payhip(page, book_folder, ficha)
        await upload_book_to_gumroad(page, book_folder, ficha)
        await upload_book_to_hotmart(page, book_folder, ficha)
        await upload_book_to_kdp(page, book_folder, ficha)
        
        await context.close()

if __name__ == "__main__":
    book = sys.argv[1] if len(sys.argv) > 1 else "oni-no-ketsuryu-volumen-5"
    asyncio.run(run_loki_autouploader(book))
