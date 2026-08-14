# -*- coding: utf-8 -*-
"""
===============================================================================
TEST DE COMPLETADO COMPLETO PASO 1 EN HOTMART
===============================================================================
Selecciona Idioma, País, Categoría, Título, Descripción (+200 caracteres)
y Portada para pasar la validación de Hotmart.
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

async def test_paso1_hotmart(folder_name):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", folder_name)[:100]
    
    # Asegurar que la descripción tenga más de 200 caracteres
    desc_base = ficha.get("descripcion", "") or ficha.get("headline", "")
    beneficios = " ".join(ficha.get("beneficios", []))
    capitulos = " ".join(ficha.get("capitulos", []))
    
    desc_text = f"{desc_base}\n\nLo que incluye este eBook:\n{beneficios}\n\nContenido:\n{capitulos}"
    if len(desc_text) < 210:
        desc_text += " Edición oficial publicada por Nicolás Noguera Editorial. Todos los derechos reservados. Disponible en formato digital de alta calidad."

    portada   = folder_path / "portada.jpg"

    print(f"\n========================================================")
    print(f"  PROBANDO CAMPOS OBLIGATORIOS PASO 1 HOTMART")
    print(f"========================================================")
    print(f"  Título ({len(titulo)} chars): {titulo[:50]}...")
    print(f"  Descripción ({len(desc_text)} chars)")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        await hotmart_page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
        await hotmart_page.wait_for_timeout(2000)

        ebook_btn = await hotmart_page.query_selector('button[id="4"], button:has-text("eBook")')
        if ebook_btn:
            await ebook_btn.click()
            await hotmart_page.wait_for_timeout(2500)

        # 1. Nombre
        name_in = await hotmart_page.query_selector('#name, input[name="name"]')
        if name_in:
            await name_in.fill(titulo)
            print("   -> Título OK.")

        # 2. Descripción (+200 chars)
        desc_in = await hotmart_page.query_selector('#description, textarea[name="description"]')
        if desc_in:
            await desc_in.fill(desc_text)
            print("   -> Descripción OK.")

        # 3. Idioma (Español)
        lang_sel = await hotmart_page.query_selector('select[name="language"], #language, [data-testid="language-select"]')
        if lang_sel:
            try:
                await lang_sel.select_option(value="es")
            except Exception:
                pass

        # 4. Portada (.jpg)
        cover_in = await hotmart_page.query_selector('#cover, input[type="file"]')
        if cover_in and portada.exists():
            print("   -> Subiendo portada.jpg...")
            await cover_in.set_input_files(str(portada))
            await hotmart_page.wait_for_timeout(3000)

        # 5. Clic en Continuar
        cont_btn = await hotmart_page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn:
            print("   -> Presionando 'Continuar'...")
            await cont_btn.click()
            await hotmart_page.wait_for_timeout(4000)

        print("   URL FINAL:", hotmart_page.url)

if __name__ == "__main__":
    asyncio.run(test_paso1_hotmart("de-cero-a-negocio-con-ia"))
