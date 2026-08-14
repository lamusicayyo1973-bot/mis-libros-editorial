# -*- coding: utf-8 -*-
"""
===============================================================================
TEST PERFECTO PASO A PASO EN HOTMART
===============================================================================
Carga 'El Algoritmo Personal' asegurando que el botón 'eBook' sea presionado
y esperando la respuesta del formulario.
===============================================================================
"""

import sys, json, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

async def test_un_libro():
    folder_path = BOOKS_DIR / "el-algoritmo-personal"
    ficha_file = folder_path / "ficha_producto.json"
    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo = ficha.get("titulo", "El Algoritmo Personal")[:100]
    desc_base = ficha.get("descripcion", "") or ficha.get("headline", "")
    beneficios = " ".join(ficha.get("beneficios", []))
    capitulos = " ".join(ficha.get("capitulos", []))
    
    desc_text = f"{desc_base}\n\nLo que incluye este eBook:\n{beneficios}\n\nContenido:\n{capitulos}\n\nEdición oficial publicada por Nicolás Noguera Editorial. Todos los derechos reservados. Disponible en formato digital."
    portada = folder_path / "portada.jpg"
    libro_file = list(folder_path.glob("*.docx"))[0]

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        print("1. Yendo a https://app.hotmart.com/products/add...")
        await page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
        await page.wait_for_timeout(2500)

        print("2. Buscando botón eBook...")
        ebook_btn = await page.wait_for_selector('button[id="4"], button:has-text("eBook")', timeout=10000)
        if ebook_btn:
            print("   -> Clickeando eBook...")
            await ebook_btn.click()
            await page.wait_for_timeout(3000)

        print("3. Buscando input de nombre...")
        name_in = await page.wait_for_selector('#name, input[name="name"]', timeout=10000)
        await name_in.fill(titulo)
        print("   -> Título cargado OK.")

        desc_in = await page.query_selector('#description, textarea[name="description"]')
        if desc_in:
            await desc_in.fill(desc_text)
            print("   -> Descripción cargada OK.")

        cat_btn = await page.query_selector('button:has-text("Literatura"), button:has-text("Negocios y Carrera")')
        if cat_btn:
            await cat_btn.click()
            print("   -> Categoría seleccionada OK.")

        cover_in = await page.query_selector('#cover, input[type="file"]')
        if cover_in and portada.exists():
            await cover_in.set_input_files(str(portada))
            print("   -> Portada cargada OK.")
            await page.wait_for_timeout(3000)

        cont_btn1 = await page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn1:
            print("4. Clic en Continuar a Precificación...")
            await cont_btn1.click()
            await page.wait_for_timeout(4000)

        print("URL DESPUES DE PASO 1:", page.url)

if __name__ == "__main__":
    asyncio.run(test_un_libro())
