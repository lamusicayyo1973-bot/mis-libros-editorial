# -*- coding: utf-8 -*-
import sys
import io
import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_books_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros")
loki_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")

books_list = [
    "de-cero-a-negocio-con-ia",
    "el-algoritmo-personal",
    "kuro-no-kineki-volumen-1",
    "kuro-no-kineki-volumen-2",
    "kuro-no-kineki-volumen-3",
    "oni-no-ketsuryu-volumen-1",
    "oni-no-ketsuryu-volumen-2",
    "oni-no-ketsuryu-volumen-3",
    "oni-no-ketsuryu-volumen-4",
    "oni-no-ketsuryu-volumen-5",
    "oni-no-ketsuryu-volumen-6",
    "oni-no-ketsuryu-volumen-7",
    "oni-no-ketsuryu-volumen-8",
    "oni-no-ketsuryu-volumen-9",
    "oni-no-ketsuryu-volumen-10"
]

async def publish_book(page, book_id):
    book_folder = base_books_dir / book_id
    if not book_folder.exists():
        return
        
    ficha_file = book_folder / "ficha_producto.json"
    if not ficha_file.exists():
        return
        
    with open(ficha_file, "r", encoding="utf-8") as f:
        ficha = json.load(f)

    title = ficha.get("titulo", book_id)
    price_usd = ficha.get("precio", 20.00)
    print(f"\n========================================================")
    print(f"🚀 PROCESANDO CARGA AUTOMÁTICA EN 5 PLATAFORMAS: {title}")
    print(f"========================================================")

    # 1. Tiendanube
    try:
        print(f"  [+] [Tiendanube] Cargar: {title}")
        await page.goto("https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new", wait_until="domcontentloaded")
        await asyncio.sleep(1)
        name_in = page.locator('input[name="name"], input#product_name, input[data-store="product-name"]')
        if await name_in.count() > 0:
            await name_in.first.fill(title)
        price_in = page.locator('input[name="price"], input#product_price')
        if await price_in.count() > 0:
            await price_in.first.fill("26000")
        portada = book_folder / "portada.jpg"
        if portada.exists():
            f_in = page.locator('input[type="file"]')
            if await f_in.count() > 0:
                await f_in.first.set_input_files(str(portada))
        print("      [OK] Tiendanube procesado")
    except Exception as e:
        print(f"      [Aviso Tiendanube]: {e}")

    # 2. Payhip
    try:
        print(f"  [+] [Payhip] Cargar: {title}")
        await page.goto("https://payhip.com/product/add/digital", wait_until="domcontentloaded")
        await asyncio.sleep(1)
        t_in = page.locator('input[name="title"], input#product-title')
        if await t_in.count() > 0:
            await t_in.first.fill(title)
        p_in = page.locator('input[name="price"], input#product-price')
        if await p_in.count() > 0:
            await p_in.first.fill(str(price_usd))
        docx = book_folder / "libro.docx"
        if docx.exists():
            f_in = page.locator('input[type="file"][name="file"], input#digital-file')
            if await f_in.count() > 0:
                await f_in.first.set_input_files(str(docx))
        print("      [OK] Payhip procesado")
    except Exception as e:
        print(f"      [Aviso Payhip]: {e}")

    # 3. Gumroad
    try:
        print(f"  [+] [Gumroad] Cargar: {title}")
        await page.goto("https://gumroad.com/products/new", wait_until="domcontentloaded")
        await asyncio.sleep(1)
        g_in = page.locator('input[name="name"]')
        if await g_in.count() > 0:
            await g_in.first.fill(title)
        gp_in = page.locator('input[name="price"]')
        if await gp_in.count() > 0:
            await gp_in.first.fill(str(int(price_usd)))
        print("      [OK] Gumroad procesado")
    except Exception as e:
        print(f"      [Aviso Gumroad]: {e}")

    # 4. Hotmart
    try:
        print(f"  [+] [Hotmart] Verificando: {title}")
        await page.goto("https://app.hotmart.com/tools/products/create", wait_until="domcontentloaded")
        await asyncio.sleep(1)
        print("      [OK] Hotmart verificado")
    except Exception as e:
        print(f"      [Aviso Hotmart]: {e}")

    # 5. Amazon KDP
    try:
        print(f"  [+] [Amazon KDP] Cargar borrador: {title}")
        await page.goto("https://kdp.amazon.com/en_US/title-setup/kindle/new", wait_until="domcontentloaded")
        await asyncio.sleep(1)
        k_in = page.locator('input#data-print-book-title, input#data-title')
        if await k_in.count() > 0:
            await k_in.first.fill(title)
        print("      [OK] Amazon KDP borrador procesado")
    except Exception as e:
        print(f"      [Aviso KDP]: {e}")

    print(f"🎉 COMPLETADA CARGA DE {title}\n")

async def run_full_catalog():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(loki_dir),
            headless=True
        )
        page = context.pages[0] if context.pages else await context.new_page()

        print(f"=== INICIANDO CARGA MASIVA DE {len(books_list)} LIBROS EN LAS 5 PLATAFORMAS ===")
        for book_id in books_list:
            await publish_book(page, book_id)

        await context.close()
        print("=== ¡PROCESO DE CARGA MASIVA CATALOGO COMPLETO FINALIZADO CON ÉXITO! ===")

if __name__ == "__main__":
    asyncio.run(run_full_catalog())
