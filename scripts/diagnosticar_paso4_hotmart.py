# -*- coding: utf-8 -*-
"""
===============================================================================
DIAGNÓSTICO EXACTO PASO A PASO EN HOTMART CON CAPTURAS
===============================================================================
Recorre los 4 pasos para un libro, toma capturas de pantalla de cada paso
y extrae los botones exactos que Hotmart exige para confirmar la publicación.
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

async def diagnostico_paso4():
    folder_path = BOOKS_DIR / "de-cero-a-negocio-con-ia"
    ficha_file = folder_path / "ficha_producto.json"
    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo = ficha.get("titulo", "De Cero a Negocio con IA")[:100]
    desc_base = ficha.get("descripcion", "") or ficha.get("headline", "")
    beneficios = " ".join(ficha.get("beneficios", []))
    capitulos = " ".join(ficha.get("capitulos", []))
    
    desc_text = f"{desc_base}\n\nLo que incluye este eBook:\n{beneficios}\n\nContenido:\n{capitulos}\n\nEdición oficial publicada por Nicolás Noguera Editorial. Todos los derechos reservados. Disponible en formato digital."
    portada = folder_path / "portada.jpg"
    libro_file = list(folder_path.glob("*.docx"))[0]

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()

        print("1. Iniciando en https://app.hotmart.com/products/add...")
        await page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Clic eBook
        ebook_btn = await page.query_selector('button[id="4"], button:has-text("eBook")')
        if ebook_btn:
            await ebook_btn.click()
            await page.wait_for_timeout(2500)

        print("2. Llenando Paso 1 (Info)...")
        await (await page.query_selector('#name, input[name="name"]')).fill(titulo)
        await (await page.query_selector('#description, textarea[name="description"]')).fill(desc_text)
        
        cat_btn = await page.query_selector('button:has-text("Literatura"), button:has-text("Negocios y Carrera")')
        if cat_btn:
            await cat_btn.click()

        cover_in = await page.query_selector('#cover, input[type="file"]')
        if cover_in and portada.exists():
            await cover_in.set_input_files(str(portada))
            await page.wait_for_timeout(2000)

        await page.screenshot(path=r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_paso1.png")
        print("   Captura Paso 1 guardada.")

        # Continuar a Paso 2
        cont_btn1 = await page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn1:
            await cont_btn1.click()
            await page.wait_for_timeout(3500)

        print("3. URL en Paso 2:", page.url)
        await page.screenshot(path=r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_paso2.png")

        # Paso 2 Moneda + Precio
        moneda_trigger = await page.query_selector('.hot-form, [class*="select"]')
        if moneda_trigger:
            await moneda_trigger.click()
            await page.wait_for_timeout(1000)
            usd_opt = await page.query_selector('div:has-text("Dólar estadounidense"), span:has-text("Dólar estadounidense")')
            if usd_opt:
                await usd_opt.click()
                await page.wait_for_timeout(1000)

        price_input = await page.query_selector('input[type="text"], input[name="price"], #price')
        if price_input:
            await price_input.fill("20.00")

        save_btn2 = await page.query_selector('button:has-text("Guardar y continuar"), button:has-text("Continuar")')
        if save_btn2:
            await save_btn2.click()
            await page.wait_for_timeout(3500)

        print("4. URL en Paso 3:", page.url)
        await page.screenshot(path=r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_paso3.png")

        # Extraer todos los botones de la pantalla en Paso 3 / Paso 4
        buttons = await page.query_selector_all('button')
        print("\nBOTONES DISPONIBLES EN PANTALLA:")
        for b in buttons:
            txt = (await b.inner_text()).strip().replace('\n', ' ')
            vis = await b.is_visible()
            ena = await b.is_enabled()
            print(f"  • Button text='{txt}' | Vis={{vis}} | Enabled={{ena}}")

if __name__ == "__main__":
    asyncio.run(diagnostico_paso4())
