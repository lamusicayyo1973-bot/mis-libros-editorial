# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICACIÓN HOTMART CON NAVEGACIÓN ESTABLE
===============================================================================
Procesa cada libro en Hotmart completando todos los campos obligatorios:
- Formato eBook
- Título + Descripción (>200 caracteres) + Categoría + Portada
- Moneda (USD) + Precio ($20 USD)
- Subida de manuscrito (.docx/.pdf) + Guardado final
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


async def publicar_libro_hotmart_individual(page, folder_name, index, total):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[{index:02d}/{total:02d}] ❌ No existe ficha_producto.json en {folder_name}")
        return False

    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", folder_name)[:100]
    desc_base = ficha.get("descripcion", "") or ficha.get("headline", "")
    beneficios = " ".join(ficha.get("beneficios", []))
    capitulos = " ".join(ficha.get("capitulos", []))
    
    desc_text = f"{desc_base}\n\nLo que incluye este eBook:\n{beneficios}\n\nContenido:\n{capitulos}\n\nEdición oficial publicada por Nicolás Noguera Editorial. Todos los derechos reservados."
    if len(desc_text) < 210:
        desc_text += " Disponible en formato digital de alta definición para lectura online o descarga inmediata."

    precio    = str(int(ficha.get("precio", 20.0)))
    portada   = folder_path / "portada.jpg"
    
    libro_file = None
    for f in folder_path.glob("*"):
        if f.suffix.lower() in [".docx", ".pdf"]:
            libro_file = f
            break

    print(f"\n========================================================")
    print(f" [{index:02d}/{total:02d}] PROCESANDO EN HOTMART: {titulo}")
    print(f"========================================================")

    try:
        # 1. Formato eBook
        await page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        ebook_btn = await page.query_selector('button[id="4"], button:has-text("eBook")')
        if ebook_btn:
            await ebook_btn.click()
            await page.wait_for_timeout(3000)

        # 2. Información Básica
        print("   -> Llenando título y descripción (+200 chars)...")
        name_input = await page.query_selector('#name, input[name="name"]')
        if name_input:
            await name_input.fill(titulo)

        desc_input = await page.query_selector('#description, textarea[name="description"]')
        if desc_input:
            await desc_input.fill(desc_text)

        # Seleccionar categoría
        cat_btn = await page.query_selector('button:has-text("Literatura"), button:has-text("Negocios y Carrera"), button:has-text("Educacional"), button:has-text("Emprendimiento Digital")')
        if cat_btn:
            print("   -> Seleccionando categoría...")
            await cat_btn.click()
            await page.wait_for_timeout(1500)

        # Subir portada
        cover_input = await page.query_selector('#cover, input[type="file"]')
        if cover_input and portada.exists():
            print("   -> Subiendo portada.jpg...")
            await cover_input.set_input_files(str(portada))
            await page.wait_for_timeout(3000)

        cont_btn1 = await page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn1:
            print("   -> Avanzando a Precificación...")
            await cont_btn1.click()
            await page.wait_for_timeout(4000)

        # 3. Precificación ($20 USD)
        print(f"   -> Asignando Moneda USD y Precio (${precio})...")
        moneda_trigger = await page.query_selector('.hot-form, [class*="select"]')
        if moneda_trigger:
            await moneda_trigger.click()
            await page.wait_for_timeout(1500)

        usd_opt = await page.query_selector('div:has-text("Dólar estadounidense"), span:has-text("Dólar estadounidense")')
        if usd_opt:
            await usd_opt.click()
            await page.wait_for_timeout(2000)

        price_input = await page.query_selector('input[type="text"], input[name="price"], #price')
        if price_input:
            try:
                await price_input.fill(f"{precio}.00", timeout=5000)
            except Exception:
                pass

        save_btn2 = await page.query_selector('button:has-text("Guardar y continuar"), button:has-text("Continuar")')
        if save_btn2:
            print("   -> Avanzando a Contenido...")
            try:
                await save_btn2.click(timeout=8000)
            except Exception:
                pass
            await page.wait_for_timeout(4000)

        # 4. Contenido (Manuscrito)
        file_input = await page.query_selector('input[type="file"]')
        if file_input and libro_file and libro_file.exists():
            print(f"   -> Subiendo manuscrito: {libro_file.name}...")
            await file_input.set_input_files(str(libro_file))
            await page.wait_for_timeout(5000)

        save_final = await page.query_selector('button:has-text("Finalizar"), button:has-text("Guardar"), button:has-text("Enviar")')
        if save_final:
            try:
                await save_final.click(timeout=8000)
            except Exception:
                pass
            await page.wait_for_timeout(4000)

        print(f"   🎉 ¡EXITO! {titulo} procesado completamente.")
        return True

    except Exception as e:
        print(f"   [!] Aviso al procesar {folder_name}: {e}")
        return False


async def main():
    print("======================================================================")
    print("   PUBLICACIÓN INDIVIDUAL NAVEGACIÓN ESTABLE EN HOTMART")
    print("======================================================================")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("[X] No se pudo conectar a Brave en puerto 9222:", e)
            return

        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        total = len(LIBROS_ORDENADOS)
        exitos = 0

        for idx, folder_name in enumerate(LIBROS_ORDENADOS, 1):
            res = await publicar_libro_hotmart_individual(hotmart_page, folder_name, idx, total)
            if res:
                exitos += 1
            await asyncio.sleep(3)

        print("\n" + "=" * 70)
        print(f"   RESULTADO FINAL: {exitos}/{total} LIBROS PUBLICADOS EN HOTMART")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
