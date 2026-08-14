# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICADOR AUTOMÁTICO EN HOTMART VÍA CDP (PUERTO 9222)
===============================================================================
Busca la pestaña logueada (app.hotmart.com) y publica cada uno de los 15 libros.
===============================================================================
"""

import sys
import os
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


async def publicar_hotmart_libro(page, folder_name, index, total):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[{index:02d}/{total:02d}] ❌ No existe ficha_producto.json en {folder_name}")
        return False

    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", folder_name)[:100]
    desc_text = ficha.get("descripcion", "") or ficha.get("headline", "")
    portada   = folder_path / "portada.jpg"

    print(f"\n========================================================")
    print(f" [{index:02d}/{total:02d}] HOTMART: {titulo}")
    print(f"========================================================")

    await page.goto("https://app.hotmart.com/products/add/4/info", wait_until="networkidle")
    await page.wait_for_timeout(2500)

    # 1. Nombre del producto
    name_input = await page.query_selector('#name, input[id="name"], input[name="name"]')
    if name_input:
        await name_input.fill(titulo)
        print("   -> Nombre del producto OK.")

    # 2. Descripción
    desc_input = await page.query_selector('#description, textarea[id="description"], textarea[name="description"]')
    if desc_input:
        await desc_input.fill(desc_text)
        print("   -> Descripción OK.")

    # 3. Portada
    cover_input = await page.query_selector('#cover, input[type="file"]')
    if cover_input and portada.exists():
        print("   -> Subiendo portada.jpg...")
        await cover_input.set_input_files(str(portada))
        await page.wait_for_timeout(3000)

    # 4. Clic en "Continuar" / "Guardar"
    save_btn = await page.query_selector('button:has-text("Continuar"), button:has-text("Guardar"), button[type="submit"]')
    if save_btn:
        print("   -> Guardando en Hotmart...")
        await save_btn.click()
        await page.wait_for_timeout(4000)
        print(f"   [OK] {titulo} procesado en Hotmart -> {page.url}")
        return True
    else:
        print("   [!] Botón Guardar no encontrado.")
        return False


async def main():
    print("======================================================================")
    print("   PUBLICADOR BATCH EN HOTMART - 15 LIBROS")
    print("======================================================================")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("[X] No se pudo conectar a Brave en el puerto 9222:", e)
            return

        context = browser.contexts[0]
        
        # Buscar pestaña que esté en app.hotmart.com
        page = None
        for pg in context.pages:
            if "app.hotmart.com" in pg.url:
                page = pg
                break
        
        if not page:
            # Buscar cualquier pestaña de hotmart
            for pg in context.pages:
                if "hotmart" in pg.url:
                    page = pg
                    break

        if not page:
            page = await context.new_page()

        print(f"Pestaña activa seleccionada: {page.url}")

        total = len(LIBROS_ORDENADOS)
        for idx, folder_name in enumerate(LIBROS_ORDENADOS, 1):
            await publicar_hotmart_libro(page, folder_name, idx, total)
            await asyncio.sleep(2)

        print("\n" + "=" * 70)
        print("   PROCESO DE HOTMART FINALIZADO")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
