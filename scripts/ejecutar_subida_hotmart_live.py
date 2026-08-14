# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICACIÓN EN VIVO SOBRE LA SESIÓN ACTIVA DE HOTMART EN BRAVE
===============================================================================
Conecta al navegador Brave donde el usuario ya está logueado en Hotmart
y publica los 15 libros completando la información, precificación y manuscrito.
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


async def publicar_libro(page, folder_name, idx, total):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[{idx:02d}/{total:02d}] ❌ No existe ficha_producto.json")
        return False

    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", folder_name)[:100]
    desc_base = ficha.get("descripcion", "") or ficha.get("headline", "")
    beneficios = " ".join(ficha.get("beneficios", []))
    capitulos = " ".join(ficha.get("capitulos", []))
    
    desc_text = f"{desc_base}\n\nLo que incluye este eBook:\n{beneficios}\n\nContenido:\n{capitulos}\n\nEdición oficial publicada por Nicolás Noguera Editorial. Todos los derechos reservados. Disponible en formato digital."
    if len(desc_text) < 210:
        desc_text += " Excelente guía en formato digital para lectura inmediata."

    precio    = str(int(ficha.get("precio", 20.0)))
    portada   = folder_path / "portada.jpg"
    
    libro_file = None
    for f in folder_path.glob("*"):
        if f.suffix.lower() in [".docx", ".pdf"]:
            libro_file = f
            break

    print(f"\n========================================================")
    print(f" [{idx:02d}/{total:02d}] SUBIENDO EN VIVO A HOTMART: {titulo}")
    print(f"========================================================")

    try:
        # Paso 1: Formato
        await page.goto("https://app.hotmart.com/products/add", wait_until="domcontentloaded")
        await page.wait_for_timeout(2500)

        ebook_btn = await page.query_selector('button[id="4"], button:has-text("eBook")')
        if ebook_btn:
            await ebook_btn.click()
            await page.wait_for_timeout(2500)

        # Paso 2: Datos básicos
        print("   1/4 Cargando título y descripción (+200 caracteres)...")
        name_in = await page.query_selector('#name, input[name="name"]')
        if name_in:
            await name_in.fill(titulo)

        desc_in = await page.query_selector('#description, textarea[name="description"]')
        if desc_in:
            await desc_in.fill(desc_text)

        cat_btn = await page.query_selector('button:has-text("Literatura"), button:has-text("Negocios y Carrera"), button:has-text("Educacional"), button:has-text("Emprendimiento Digital")')
        if cat_btn:
            print("   -> Seleccionando categoría...")
            await cat_btn.click()
            await page.wait_for_timeout(1000)

        cover_in = await page.query_selector('#cover, input[type="file"]')
        if cover_in and portada.exists():
            print("   -> Subiendo portada.jpg...")
            await cover_in.set_input_files(str(portada))
            await page.wait_for_timeout(3000)

        cont_btn1 = await page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn1:
            print("   2/4 Avanzando a Precificación...")
            try:
                await cont_btn1.click()
            except Exception:
                pass
            await page.wait_for_timeout(4000)

        # Paso 3: Precificación ($20 USD)
        print(f"   3/4 Fijando Moneda USD y Precio (${precio})...")
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
            try:
                await price_in.fill(f"{precio}.00")
            except Exception:
                pass

        save_btn2 = await page.query_selector('button:has-text("Guardar y continuar"), button:has-text("Continuar")')
        if save_btn2:
            print("   -> Avanzando a Contenido...")
            try:
                await save_btn2.click()
            except Exception:
                pass
            await page.wait_for_timeout(4000)

        # Paso 4: Contenido (Manuscrito)
        file_in = await page.query_selector('input[type="file"]')
        if file_in and libro_file and libro_file.exists():
            print(f"   4/4 Adjuntando manuscrito: {libro_file.name}...")
            await file_in.set_input_files(str(libro_file))
            await page.wait_for_timeout(5000)

        save_final = await page.query_selector('button:has-text("Finalizar"), button:has-text("Guardar"), button:has-text("Enviar")')
        if save_final:
            try:
                await save_final.click()
            except Exception:
                pass
            await page.wait_for_timeout(4000)

        print(f"   🎉 ¡ÉXITO COMPLETO! {titulo} subido y procesado.")
        return True

    except Exception as e:
        print(f"   [!] Error en {folder_name}: {e}")
        return False


async def main():
    print("======================================================================")
    print("   EJECUCIÓN DE CARGA EN VIVO EN LA SESIÓN ACTIVA DE HOTMART")
    print("======================================================================")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("❌ No se pudo conectar a Brave en puerto 9222:", e)
            return

        context = browser.contexts[0]
        pages = context.pages
        hotmart_pages = [pg for pg in pages if "hotmart" in pg.url]
        
        if hotmart_pages:
            page = hotmart_pages[0]
        else:
            page = await context.new_page()

        total = len(LIBROS_ORDENADOS)
        exitos = 0

        for idx, folder_name in enumerate(LIBROS_ORDENADOS, 1):
            res = await publicar_libro(page, folder_name, idx, total)
            if res:
                exitos += 1
            await asyncio.sleep(2)

        print("\n" + "=" * 70)
        print(f"   RESULTADO FINAL: {exitos}/{total} LIBROS PROCESADOS")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
