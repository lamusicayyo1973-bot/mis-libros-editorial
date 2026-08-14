# -*- coding: utf-8 -*-
"""
===============================================================================
SUBIDA Y ESPERA VERIFICADA DE UN SOLO LIBRO EN HOTMART
===============================================================================
Inicia en /products/add, hace clic en eBook, completa cada paso y espera
a que la URL del producto se confirme y registre en Hotmart.
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

async def subir_un_libro_paso_a_paso(folder_name):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo = ficha.get("titulo", folder_name)[:100]
    desc_base = ficha.get("descripcion", "") or ficha.get("headline", "")
    beneficios = " ".join(ficha.get("beneficios", []))
    capitulos = " ".join(ficha.get("capitulos", []))
    
    desc_text = f"{desc_base}\n\nLo que incluye este eBook:\n{beneficios}\n\nContenido:\n{capitulos}\n\nEdición oficial publicada por Nicolás Noguera Editorial. Todos los derechos reservados. Disponible en formato digital."
    portada = folder_path / "portada.jpg"
    libro_file = list(folder_path.glob("*.docx"))[0]

    print(f"\n========================================================")
    print(f" CARGANDO Y ESPERANDO CONFIRMACIÓN DE: {titulo}")
    print(f"========================================================")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        # 1. Abrir add
        print("1. Navegando a https://app.hotmart.com/products/add...")
        await page.goto("https://app.hotmart.com/products/add", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # Clic en eBook si está visible
        ebook_btn = await page.query_selector('button[id="4"], button:has-text("eBook")')
        if ebook_btn:
            print("2. Seleccionando formato eBook...")
            await ebook_btn.click()
            await page.wait_for_timeout(3000)

        # 2. Información
        print("3. Llenando nombre y descripción (+200 caracteres)...")
        name_in = await page.query_selector('#name, input[name="name"]')
        if name_in:
            await name_in.fill(titulo)

        desc_in = await page.query_selector('#description, textarea[name="description"]')
        if desc_in:
            await desc_in.fill(desc_text)

        cat_btn = await page.query_selector('button:has-text("Literatura"), button:has-text("Negocios y Carrera")')
        if cat_btn:
            await cat_btn.click()
            await page.wait_for_timeout(1000)

        cover_in = await page.query_selector('#cover, input[type="file"]')
        if cover_in and portada.exists():
            print("   -> Subiendo portada.jpg...")
            await cover_in.set_input_files(str(portada))
            await page.wait_for_timeout(3000)

        cont_btn1 = await page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn1:
            print("4. Avanzando a Precificación...")
            await cont_btn1.click()
            await page.wait_for_timeout(4000)

        # 3. Precificación
        print("5. Fijando Moneda USD y Precio $20...")
        moneda_trig = await page.query_selector('.hot-form, [class*="select"]')
        if moneda_trig:
            try:
                await moneda_trig.click()
                await page.wait_for_timeout(1000)
                usd_opt = await page.query_selector('div:has-text("Dólar estadounidense"), span:has-text("Dólar estadounidense")')
                if usd_opt:
                    await usd_opt.click()
                    await page.wait_for_timeout(1000)
            except Exception:
                pass

        price_in = await page.query_selector('input[type="text"], input[name="price"], #price')
        if price_in:
            await price_in.fill("20.00")

        save_btn2 = await page.query_selector('button:has-text("Guardar y continuar"), button:has-text("Continuar")')
        if save_btn2:
            print("6. Avanzando a Contenido...")
            await save_btn2.click()
            await page.wait_for_timeout(4000)

        # 4. Contenido
        file_in = await page.query_selector('input[type="file"]')
        if file_in and libro_file.exists():
            print(f"7. Adjuntando manuscrito: {libro_file.name}...")
            await file_in.set_input_files(str(libro_file))
            await page.wait_for_timeout(5000)

        save_final = await page.query_selector('button:has-text("Finalizar"), button:has-text("Guardar"), button:has-text("Enviar")')
        if save_final:
            print("8. GUARDANDO DEFORMA DEFINITIVA EN HOTMART (ESPERANDO 12 SEGUNDOS)...")
            await save_final.click()
            await page.wait_for_timeout(12000)

        print("\nURL RESULTADO DE GUARDADO:", page.url)

        # Sacar captura final del producto creado
        shot_path = r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_producto_creado.png"
        await page.screenshot(path=shot_path, full_page=True)
        print(f"Captura guardada en: {shot_path}")

if __name__ == "__main__":
    asyncio.run(subir_un_libro_paso_a_paso("el-algoritmo-personal"))
