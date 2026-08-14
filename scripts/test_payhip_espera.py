# -*- coding: utf-8 -*-
"""
===============================================================================
TEST DE PUBLICACIÓN CON ESPERA DE CARGA DE ARCHIVO EN PAYHIP
===============================================================================
Sube 'el-algoritmo-personal' en Payhip y espera a que la barra de progreso
de Payhip termine el upload del manuscrito y confirme la publicación.
===============================================================================
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

def armar_html_descripcion(ficha):
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

async def test_payhip_con_espera(folder_name):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
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
    print(f"  PROBANDO CON ESPERA DE CARGA: {titulo}")
    print(f"========================================================")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if 'payhip.com' in pg.url][0]

        await payhip_page.goto('https://payhip.com/product/add/digital', wait_until='networkidle')
        await payhip_page.wait_for_timeout(1500)

        # 1. Subir manuscrito digital (.docx / .pdf)
        file_inputs = await payhip_page.query_selector_all('input[type="file"]')
        if file_inputs and libro_file and libro_file.exists():
            print(f"  -> Seleccionando manuscrito: {libro_file.name}")
            await file_inputs[0].set_input_files(str(libro_file))
            print("  -> Esperando a que el archivo cargue en Payhip (5s)...")
            await payhip_page.wait_for_timeout(5000)

        # 2. Título
        title_el = await payhip_page.query_selector('#p_name, input[name="p_name"]')
        if title_el:
            await title_el.fill(titulo)
            print("  -> Título ingresado.")

        # 3. Precio
        price_el = await payhip_page.query_selector('#p_price, input[name="p_price"]')
        if price_el:
            await price_el.fill(precio)
            print("  -> Precio ingresado.")

        # 4. Portada
        if len(file_inputs) > 1 and portada.exists():
            print("  -> Seleccionando portada.jpg...")
            await file_inputs[1].set_input_files(str(portada))
            await payhip_page.wait_for_timeout(3000)

        # 5. Descripción HTML
        editor = await payhip_page.query_selector('.ql-editor')
        if editor:
            await editor.evaluate("(el, html) => el.innerHTML = html", desc_html)
            print("  -> Descripción ingresada.")

        # 6. Clic en "Add Product" y ESPERAR RESULTADO
        print("\n  -> Presionando botón de envío 'Add Product'...")
        submit_btn = await payhip_page.query_selector('#btn-add-product, button[type="submit"].js-submit-btn, button.btn-primary')
        if submit_btn:
            await submit_btn.click()
            print("  -> Botón clickeado. Esperando confirmación de Payhip (hasta 20 segundos)...")

            # Esperar a que la URL cambie o aparezca cartel de éxito
            try:
                await payhip_page.wait_for_url(lambda u: 'product/add' not in u, timeout=20000)
                print(f"  🎉 ¡EXITO! Redirigido a: {payhip_page.url}")
            except Exception as e:
                print(f"  [!] URL actual después de 20s: {payhip_page.url}")

if __name__ == "__main__":
    asyncio.run(test_payhip_con_espera("el-algoritmo-personal"))
