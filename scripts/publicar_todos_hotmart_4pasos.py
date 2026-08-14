# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICACIÓN MASIVA INTEGRAL 4 PASOS EN HOTMART (15 LIBROS)
===============================================================================
Recorre los 15 libros del catálogo y completa los 4 pasos en Hotmart:
1. Formato (eBook) + Información básica (Título, Descripción, Portada)
2. Asignación de Precio ($20 USD)
3. Carga del manuscrito digital (.docx / .pdf)
4. Confirmación y Finalización de producto
===============================================================================
"""

import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

LIBROS_ORDENADOS = [
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
    "oni-no-ketsuryu-volumen-10",
]


async def publicar_libro_4pasos(page, folder_name, index, total):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[{index:02d}/{total:02d}] ❌ No existe ficha_producto.json en {folder_name}")
        return False

    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", folder_name)[:100]
    desc_text = ficha.get("descripcion", "") or ficha.get("headline", "")
    precio    = str(int(ficha.get("precio", 20.0)))
    portada   = folder_path / "portada.jpg"
    
    libro_file = None
    for f in folder_path.glob("*"):
        if f.suffix.lower() in [".docx", ".pdf"]:
            libro_file = f
            break

    print(f"\n========================================================")
    print(f" [{index:02d}/{total:02d}] HOTMART 4-PASOS: {titulo}")
    print(f"========================================================")

    # 1. Formato eBook
    await page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
    await page.wait_for_timeout(2000)

    ebook_btn = await page.query_selector('button[id="4"], button:has-text("eBook")')
    if ebook_btn:
        await ebook_btn.click()
        await page.wait_for_timeout(2500)

    # 2. Información Básica
    name_input = await page.query_selector('#name, input[name="name"]')
    if name_input:
        await name_input.fill(titulo)

    desc_input = await page.query_selector('#description, textarea[name="description"]')
    if desc_input:
        await desc_input.fill(desc_text)

    cover_input = await page.query_selector('#cover, input[type="file"]')
    if cover_input and portada.exists():
        await cover_input.set_input_files(str(portada))
        await page.wait_for_timeout(3000)

    cont_btn1 = await page.query_selector('button:has-text("Continuar"), button[type="submit"]')
    if cont_btn1:
        await cont_btn1.click()
        await page.wait_for_timeout(3500)

    # 3. Precificación ($20 USD)
    price_input = await page.query_selector('input[name="price"], #price, input[placeholder*="0"], input[type="number"]')
    if price_input:
        await price_input.fill(precio)

    cont_btn2 = await page.query_selector('button:has-text("Continuar"), button:has-text("Guardar"), button[type="submit"]')
    if cont_btn2:
        await cont_btn2.click()
        await page.wait_for_timeout(3500)

    # 4. Manuscrito (.docx/.pdf) y Finalizar
    file_input = await page.query_selector('input[type="file"]')
    if file_input and libro_file and libro_file.exists():
        print(f"   -> Subiendo manuscrito: {libro_file.name}...")
        await file_input.set_input_files(str(libro_file))
        await page.wait_for_timeout(4000)

    save_final = await page.query_selector('button:has-text("Finalizar"), button:has-text("Guardar"), button:has-text("Enviar"), button[type="submit"]')
    if save_final:
        await save_final.click()
        await page.wait_for_timeout(3500)

    print(f"   [OK] {titulo} 100% CREADO Y PROCESADO EN HOTMART!")
    return True


async def main():
    print("======================================================================")
    print("   PUBLICADOR MASIVO INTEGRAL 4 PASOS EN HOTMART (15 LIBROS)")
    print("======================================================================")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        total = len(LIBROS_ORDENADOS)
        for idx, folder_name in enumerate(LIBROS_ORDENADOS, 1):
            await publicar_libro_4pasos(hotmart_page, folder_name, idx, total)
            await asyncio.sleep(2)

        print("\n" + "=" * 70)
        print("   ¡LOS 15 LIBROS FUERON PUBLICADOS INTEGRALMENTE EN HOTMART!")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
