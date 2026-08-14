# -*- coding: utf-8 -*-
"""
===============================================================================
TEST DE SELECCIÓN DE CATEGORÍA E IDIOMA EN HOTMART
===============================================================================
Prueba la selección de 'Literatura', 'Español' y 'Argentina' para avanzar.
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

async def test_hotmart_categoria():
    folder_path = BOOKS_DIR / "de-cero-a-negocio-con-ia"
    ficha_file = folder_path / "ficha_producto.json"
    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", "De Cero a Negocio con IA")[:100]
    desc_base = ficha.get("descripcion", "") or ficha.get("headline", "")
    beneficios = " ".join(ficha.get("beneficios", []))
    capitulos = " ".join(ficha.get("capitulos", []))
    
    desc_text = f"{desc_base}\n\nLo que incluye este eBook:\n{beneficios}\n\nContenido:\n{capitulos}\n\nEdición oficial publicada por Nicolás Noguera Editorial. Todos los derechos reservados. Disponible en formato digital."
    portada   = folder_path / "portada.jpg"

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

        # 1. Nombre y Descripción (+200 chars)
        name_in = await hotmart_page.query_selector('#name, input[name="name"]')
        if name_in:
            await name_in.fill(titulo)

        desc_in = await hotmart_page.query_selector('#description, textarea[name="description"]')
        if desc_in:
            await desc_in.fill(desc_text)

        # 2. Clic en Categoría (ej: Literatura / Negocios y Carrera)
        cat_btn = await hotmart_page.query_selector('button:has-text("Literatura"), button:has-text("Negocios y Carrera"), button:has-text("Educacional")')
        if cat_btn:
            print("   -> Seleccionando categoría...")
            await cat_btn.click()
            await hotmart_page.wait_for_timeout(1000)

        # 3. Portada
        cover_in = await hotmart_page.query_selector('#cover, input[type="file"]')
        if cover_in and portada.exists():
            print("   -> Subiendo portada.jpg...")
            await cover_in.set_input_files(str(portada))
            await hotmart_page.wait_for_timeout(3000)

        # 4. Continuar
        cont_btn = await hotmart_page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn:
            print("   -> Presionando 'Continuar'...")
            await cont_btn.click()
            await hotmart_page.wait_for_timeout(4000)

        print("   URL RESULTADO:", hotmart_page.url)

if __name__ == "__main__":
    asyncio.run(test_hotmart_categoria())
