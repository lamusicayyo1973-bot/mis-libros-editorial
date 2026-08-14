# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICADOR AUTOMÁTICO EN PAYHIP Y HOTMART VÍA CDP (PUERTO 9222)
===============================================================================
Conecta al navegador Brave abierto en el puerto 9222 y automatiza la
publicación de libros digitales en Payhip y Hotmart omitiendo Cloudflare.
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

def armar_html_descripcion(ficha):
    """Genera HTML enriquecido para la descripción del libro."""
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


async def publicar_en_payhip(page, folder_path):
    """Publica un libro en Payhip utilizando la página activa."""
    ficha_file = folder_path / "ficha_producto.json"
    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo      = ficha.get("titulo", folder_path.name)
    precio      = str(int(ficha.get("precio", 20.0)))
    desc_html   = armar_html_descripcion(ficha)
    portada_img = folder_path / "portada.jpg"
    
    # Buscar manuscrito docx o pdf
    libro_file = None
    for ext in ["libro.docx", "libro.pdf", "*.docx", "*.pdf"]:
        matches = list(folder_path.glob(ext))
        if matches:
            libro_file = matches[0]
            break

    print(f"\n[PAYHIP] Procesando: {titulo}")
    print(f"  -> Portada: {portada_img.name if portada_img.exists() else 'NO EXISTE'}")
    print(f"  -> Archivo libro: {libro_file.name if libro_file else 'NO ENCONTRADO'}")

    # Navegar a la página de agregar producto digital si no estamos ahí
    if "payhip.com/products/add/digital" not in page.url:
        await page.goto("https://payhip.com/products/add/digital", wait_until="networkidle")

    await page.wait_for_timeout(2000)

    # 1. Subir archivo digital manuscrito (.docx/.pdf)
    if libro_file and libro_file.exists():
        print("  -> Subiendo manuscrito digital...")
        file_input = await page.query_selector('input[type="file"][name="file"], input[type="file"]')
        if file_input:
            await file_input.set_input_files(str(libro_file))
            await page.wait_for_timeout(3000)

    # 2. Título
    title_input = await page.query_selector('input[name="title"], #product-title')
    if title_input:
        await title_input.fill(titulo)

    # 3. Precio
    price_input = await page.query_selector('input[name="price"], #product-price')
    if price_input:
        await price_input.fill(precio)

    # 4. Portada
    if portada_img.exists():
        print("  -> Subiendo portada.jpg...")
        cover_input = await page.query_selector('input[type="file"][name="cover"], input[name="cover_file"], input[type="file"]')
        if cover_input:
            try:
                await cover_input.set_input_files(str(portada_img))
                await page.wait_for_timeout(2000)
            except Exception as e:
                print("  [!] No se pudo subir portada por selector directo:", e)

    # 5. Descripción
    desc_elem = await page.query_selector('.ql-editor, .note-editable, div[contenteditable="true"], textarea[name="description"]')
    if desc_elem:
        tag = await desc_elem.evaluate("el => el.tagName")
        if tag == "DIV" or await desc_elem.evaluate("el => el.isContentEditable"):
            await desc_elem.evaluate(f"(el, html) => el.innerHTML = html", desc_html)
        else:
            await desc_elem.fill(desc_html)

    print("  [OK] Campos completados en Payhip. Revisá y presioná 'Add Product' o confirma.")


async def main():
    print("=" * 70)
    print("  CONECTANDO A NAVEGADOR VÍA CDP (PUERTO 9222)")
    print("=" * 70)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("\n[X] No se pudo conectar a Chrome/Brave en el puerto 9222.")
            print("    Asegurate de haber ejecutado 'Iniciar-Navegador-Editorial-Debug.bat'")
            print("    Detalle:", e)
            return

        context = browser.contexts[0]
        pages = context.pages

        print(f"\n[OK] Conectado exitosamente. Pestañas abiertas: {len(pages)}")
        for idx, pg in enumerate(pages, 1):
            print(f"  {idx}. [{pg.title()[:40]}] -> {pg.url}")

        # Buscar pestaña de Payhip o abrir una nueva
        payhip_page = None
        for pg in pages:
            if "payhip.com" in pg.url:
                payhip_page = pg
                break

        if not payhip_page:
            payhip_page = await context.new_page()
            await payhip_page.goto("https://payhip.com/dashboard")

        print("\n--- INICIANDO PROCESAMIENTO EN PAYHIP ---")
        # Listar carpetas de libros
        for folder in sorted(BOOKS_DIR.glob("*")):
            if folder.is_dir() and (folder / "ficha_producto.json").exists():
                await publicar_en_payhip(payhip_page, folder)
                input("\nPresioná ENTER en la consola para pasar al siguiente libro...")

if __name__ == "__main__":
    asyncio.run(main())
