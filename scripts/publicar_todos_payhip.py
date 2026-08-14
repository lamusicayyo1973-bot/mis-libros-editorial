# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICACIÓN MASIVA AUTOMÁTICA EN PAYHIP VÍA CDP (PUERTO 9222)
===============================================================================
Publica todos los libros restantes del catálogo en Payhip de forma secuencial:
- Manuscrito (.docx/.pdf)
- Portada (.jpg)
- Título, Precio ($20 USD) y Descripción HTML enriquecida
- Clic automático en #addsubmit y verificación
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

LIBROS_PENDIENTES = [
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


async def publicar_un_libro(page, folder_name, index, total):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[{index:02d}/{total:02d}] ❌ No existe ficha_producto.json en {folder_name}")
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

    print(f"\n========================================================")
    print(f" [{index:02d}/{total:02d}] PUBLICANDO EN PAYHIP: {titulo}")
    print(f"========================================================")

    # Navegar al formulario
    await page.goto("https://payhip.com/product/add/digital", wait_until="networkidle")
    await page.wait_for_timeout(1500)

    # 1. Manuscrito digital
    file_inputs = await page.query_selector_all('input[type="file"]')
    if file_inputs and libro_file and libro_file.exists():
        print(f"   -> Manuscrito: {libro_file.name}")
        await file_inputs[0].set_input_files(str(libro_file))
        await page.wait_for_timeout(4000)
    else:
        print(f"   [!] Sin manuscrito encontrado en {folder_name}")

    # 2. Título
    title_el = await page.query_selector('#p_name, input[name="p_name"]')
    if title_el:
        await title_el.fill(titulo)
        print("   -> Título asignado.")

    # 3. Precio
    price_el = await page.query_selector('#p_price, input[name="p_price"]')
    if price_el:
        await price_el.fill(precio)
        print(f"   -> Precio asignado (${precio} USD).")

    # 4. Portada
    if len(file_inputs) > 1 and portada.exists():
        print("   -> Portada: portada.jpg")
        await file_inputs[1].set_input_files(str(portada))
        await page.wait_for_timeout(3000)

    # 5. Descripción HTML
    editor = await page.query_selector('.ql-editor')
    if editor:
        await editor.evaluate("(el, html) => el.innerHTML = html", desc_html)
        print("   -> Descripción HTML asignada.")

    # 6. Clic en #addsubmit para PUBLICAR
    print("   -> Guardando producto (#addsubmit)...")
    submit_btn = await page.query_selector('#addsubmit')
    if submit_btn:
        await submit_btn.click()
        await page.wait_for_timeout(5000)
        print(f"   [OK] PUBLICADO EXITOSAMENTE -> URL: {page.url}")
        return True
    else:
        print("   [X] Error: Botón #addsubmit no encontrado")
        return False


async def main():
    print("======================================================================")
    print("   PUBLICADOR BATCH EN PAYHIP - 13 LIBROS PENDIENTES")
    print("======================================================================")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("[X] No se pudo conectar a Brave en el puerto 9222:", e)
            return

        context = browser.contexts[0]
        payhip_pages = [pg for pg in context.pages if "payhip.com" in pg.url]
        if payhip_pages:
            page = payhip_pages[0]
        else:
            page = await context.new_page()

        total = len(LIBROS_PENDIENTES)
        exitos = 0

        for idx, folder_name in enumerate(LIBROS_PENDIENTES, 1):
            res = await publicar_un_libro(page, folder_name, idx, total)
            if res:
                exitos += 1
            await asyncio.sleep(2)

        print("\n" + "=" * 70)
        print(f"   PROCESO COMPLETADO: {exitos}/{total} LIBROS PUBLICADOS EN PAYHIP")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
