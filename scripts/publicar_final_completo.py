# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICADOR DEFINITIVO CON GUARDADO FINAL (PAYHIP & HOTMART VÍA CDP)
===============================================================================
Llena los campos Y presiona el botón de 'Agregar Producto' / 'Guardar'
para que los libros queden 100% publicados en el listado de tus cuentas.
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


def armar_html_descripcion(ficha):
    """Genera HTML enriquecido con la sinopsis, beneficios e índice."""
    headline   = ficha.get("headline", "")
    desc       = ficha.get("descripcion", "")
    beneficios = ficha.get("beneficios", [])
    capitulos  = ficha.get("capitulos", [])
    autor      = ficha.get("autor", "Nicolás Noguera")

    html = []
    if headline:
        html.append(f"<p><strong>✨ {headline}</strong></p><hr>")
    if desc:
        html.append(f"<h3>📖 Sinopsis</h3><p>{desc}</p>")
    if beneficios:
        html.append("<h3>✨ Lo que incluye este eBook</h3><ul>")
        for b in beneficios:
            html.append(f"<li>{b}</li>")
        html.append("</ul>")
    if capitulos:
        html.append("<h3>📑 Contenido y Capítulos</h3><ul>")
        for c in capitulos:
            html.append(f"<li>{c}</li>")
        html.append("</ul>")

    html.append(f"<br><p><strong>Autor:</strong> {autor}<br><strong>Editorial:</strong> Nicolás Noguera Editorial</p>")
    return "\n".join(html)


async def publicar_payhip_completo(page, folder_name):
    """Llena el formulario en Payhip Y presiona 'Add Product' para publicarlo oficialmente."""
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"  [X] Payhip: No existe ficha_producto.json en {folder_name}")
        return False

    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", folder_name)
    precio    = str(int(ficha.get("precio", 20.0)))
    desc_html = armar_html_descripcion(ficha)
    portada   = folder_path / "portada.jpg"
    
    libro_file = None
    for f in folder_path.glob("*"):
        if f.suffix.lower() in [".docx", ".pdf"]:
            libro_file = f
            break

    print(f"\n🔹 [PAYHIP] Publicando: {titulo}")
    await page.goto("https://payhip.com/product/add/digital", wait_until="networkidle")
    await page.wait_for_timeout(1500)

    # 1. Subir manuscrito digital (.docx / .pdf)
    file_inputs = await page.query_selector_all('input[type="file"]')
    if file_inputs and libro_file and libro_file.exists():
        print(f"   -> Subiendo manuscrito ({libro_file.name})...")
        await file_inputs[0].set_input_files(str(libro_file))
        await page.wait_for_timeout(2500)

    # 2. Título
    title_el = await page.query_selector('#p_name, input[name="p_name"]')
    if title_el:
        await title_el.fill(titulo)

    # 3. Precio
    price_el = await page.query_selector('#p_price, input[name="p_price"]')
    if price_el:
        await price_el.fill(precio)

    # 4. Portada
    if len(file_inputs) > 1 and portada.exists():
        print(f"   -> Subiendo portada.jpg...")
        await file_inputs[1].set_input_files(str(portada))
        await page.wait_for_timeout(2500)

    # 5. Descripción HTML
    editor = await page.query_selector('.ql-editor')
    if editor:
        await editor.evaluate("(el, html) => el.innerHTML = html", desc_html)

    await page.wait_for_timeout(1000)

    # 6. Hacer clic en "Add Product" para GUARDAR Y PUBLICAR OFICIALMENTE
    print("   -> Haciendo clic en 'Add Product' para confirmar publicación...")
    submit_btn = await page.query_selector('#btn-add-product, button[type="submit"].js-submit-btn, button:has-text("Add Product")')
    if submit_btn:
        await submit_btn.click()
        await page.wait_for_timeout(4000)

    print(f"   🎉 [PUBLICADO EN PAYHIP] {titulo}")
    return True


async def publicar_hotmart_completo(page, folder_name):
    """Llena el formulario en Hotmart Y presiona 'Continuar' para guardarlo."""
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"  [X] Hotmart: No existe ficha_producto.json en {folder_name}")
        return False

    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", folder_name)
    desc_text = ficha.get("descripcion", "") or ficha.get("headline", "")
    portada   = folder_path / "portada.jpg"

    print(f"\n🔸 [HOTMART] Publicando: {titulo}")
    await page.goto("https://app.hotmart.com/products/add/4/info", wait_until="networkidle")
    await page.wait_for_timeout(2000)

    # 1. Nombre del producto (máx 100 chars)
    name_input = await page.query_selector('#name, input[id="name"]')
    if name_input:
        await name_input.fill(titulo[:100])

    # 2. Descripción
    desc_input = await page.query_selector('#description, textarea[id="description"]')
    if desc_input:
        await desc_input.fill(desc_text)

    # 3. Portada
    cover_input = await page.query_selector('#cover, input[type="file"]')
    if cover_input and portada.exists():
        print("   -> Subiendo portada.jpg...")
        await cover_input.set_input_files(str(portada))
        await page.wait_for_timeout(2500)

    # 4. Guardar / Continuar
    save_btn = await page.query_selector('button:has-text("Continuar"), button:has-text("Guardar"), button[type="submit"]')
    if save_btn:
        print("   -> Guardando en Hotmart...")
        await save_btn.click()
        await page.wait_for_timeout(3000)

    print(f"   🎉 [PUBLICADO EN HOTMART] {titulo}")
    return True


async def main():
    print("=" * 70)
    print("  AUTOPUBLISHER COMPLETO CON GUARDADO FINAL")
    print("=" * 70)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("\n[X] Brave no está abierto con puerto 9222.")
            print("    Ejecutá 'Iniciar-Navegador-Editorial-Debug.bat' para abrirlo.")
            return

        context = browser.contexts[0]
        pages = context.pages

        payhip_page = None
        hotmart_page = None

        for pg in pages:
            if "payhip.com" in pg.url:
                payhip_page = pg
            elif "hotmart.com" in pg.url:
                hotmart_page = pg

        if not payhip_page:
            payhip_page = await context.new_page()

        if not hotmart_page:
            hotmart_page = await context.new_page()

        print("\nOpciones de publicación:")
        print(" [1] Publicar de a 1 libro con confirmación final")
        print(" [2] Publicación masiva automatizada de TODOS los libros (1-15)")

        opc = input("\nSeleccioná opción (1 o 2): ").strip() or "1"

        if opc == "1":
            for idx, name in enumerate(LIBROS_ORDENADOS, 1):
                print(f"\n========================================================")
                print(f" PROCESANDO LIBRO [{idx:02d}/15]: {name}")
                print(f"========================================================")
                await publicar_payhip_completo(payhip_page, name)
                await publicar_hotmart_completo(hotmart_page, name)
                
                cont = input("\n👉 Libro publicado. ¿Pasar al siguiente libro? (ENTER=sí / q=salir): ")
                if cont.lower() == 'q':
                    break

        elif opc == "2":
            for idx, name in enumerate(LIBROS_ORDENADOS, 1):
                print(f"\n========================================================")
                print(f" MASIVO [{idx:02d}/15]: {name}")
                print(f"========================================================")
                await publicar_payhip_completo(payhip_page, name)
                await publicar_hotmart_completo(hotmart_page, name)

if __name__ == "__main__":
    asyncio.run(main())
