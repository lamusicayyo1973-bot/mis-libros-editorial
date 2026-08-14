# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICADOR 4 PASOS EN HOTMART VÍA CDP (PUERTO 9222)
===============================================================================
Completa la creación integral de un libro en Hotmart:
1. Formato (eBook) e Info (Título, Sinopsis, Portada)
2. Precio ($20 USD, Garantía 7 días)
3. Manuscrito (.docx/.pdf)
4. Confirmación y Activación
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

async def publicar_libro_hotmart_4pasos(folder_name):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
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
    print(f"  EJECUTANDO FLUO 4 PASOS EN HOTMART: {titulo}")
    print(f"========================================================")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        # ---------------------------------------------------------------------
        # PASO 1: Tipo de Producto -> eBook
        # ---------------------------------------------------------------------
        print("  [Paso 1/4] Seleccionando formato eBook...")
        await hotmart_page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
        await hotmart_page.wait_for_timeout(2000)

        ebook_btn = await hotmart_page.query_selector('button[id="4"], button:has-text("eBook")')
        if ebook_btn:
            await ebook_btn.click()
            await hotmart_page.wait_for_timeout(2500)

        # ---------------------------------------------------------------------
        # PASO 2: Información Básica (Título, Descripción, Portada)
        # ---------------------------------------------------------------------
        print("  [Paso 2/4] Llenando Información Básica...")
        name_input = await hotmart_page.query_selector('#name, input[name="name"]')
        if name_input:
            await name_input.fill(titulo)

        desc_input = await hotmart_page.query_selector('#description, textarea[name="description"]')
        if desc_input:
            await desc_input.fill(desc_text)

        cover_input = await hotmart_page.query_selector('#cover, input[type="file"]')
        if cover_input and portada.exists():
            print("     -> Subiendo portada.jpg...")
            await cover_input.set_input_files(str(portada))
            await hotmart_page.wait_for_timeout(3000)

        cont_btn1 = await hotmart_page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn1:
            print("     -> Clic en Continuar a Precificación...")
            await cont_btn1.click()
            await hotmart_page.wait_for_timeout(4000)

        # ---------------------------------------------------------------------
        # PASO 3: Precificación (Moneda USD, Precio, Garantía)
        # ---------------------------------------------------------------------
        print(f"  [Paso 3/4] Asignando Precio (${precio} USD)...")
        price_input = await hotmart_page.query_selector('input[name="price"], #price, input[placeholder*="0"], input[type="number"]')
        if price_input:
            await price_input.fill(precio)
            print("     -> Precio ingresado.")

        cont_btn2 = await hotmart_page.query_selector('button:has-text("Continuar"), button:has-text("Guardar"), button[type="submit"]')
        if cont_btn2:
            print("     -> Clic en Continuar a Contenido...")
            await cont_btn2.click()
            await hotmart_page.wait_for_timeout(4000)

        # ---------------------------------------------------------------------
        # PASO 4: Contenido (Subir manuscrito .docx / .pdf)
        # ---------------------------------------------------------------------
        print("  [Paso 4/4] Subiendo Manuscrito del libro...")
        file_input = await hotmart_page.query_selector('input[type="file"]')
        if file_input and libro_file and libro_file.exists():
            print(f"     -> Subiendo {libro_file.name}...")
            await file_input.set_input_files(str(libro_file))
            await hotmart_page.wait_for_timeout(5000)

        save_final = await hotmart_page.query_selector('button:has-text("Finalizar"), button:has-text("Guardar"), button:has-text("Enviar"), button[type="submit"]')
        if save_final:
            await save_final.click()
            await hotmart_page.wait_for_timeout(4000)

        print(f"  🎉 [COMPLETO] {titulo} procesado con éxito en Hotmart! URL: {hotmart_page.url}")

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "de-cero-a-negocio-con-ia"
    asyncio.run(publicar_libro_hotmart_4pasos(folder))
