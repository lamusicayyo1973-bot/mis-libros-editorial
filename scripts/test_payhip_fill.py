# -*- coding: utf-8 -*-
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

async def test_fill_payhip(folder_name):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo    = ficha.get("titulo", folder_name)
    precio    = str(int(ficha.get("precio", 20.0)))
    desc_html = armar_html_descripcion(ficha)
    portada   = folder_path / "portada.jpg"
    
    # Find manuscript (.docx or .pdf)
    libro_file = None
    for f in folder_path.glob("*"):
        if f.suffix.lower() in [".docx", ".pdf"]:
            libro_file = f
            break

    print(f"=== PROBANDO LLENADO EN PAYHIP PARA: {folder_name} ===")
    print(f"  Título: {titulo}")
    print(f"  Precio: ${precio} USD")
    print(f"  Manuscr: {libro_file}")
    print(f"  Portada: {portada}")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if 'payhip.com' in pg.url][0]

        await payhip_page.goto('https://payhip.com/product/add/digital', wait_until='networkidle')
        await payhip_page.wait_for_timeout(1000)

        # 1. Manuscrito (.docx / .pdf)
        file_inputs = await payhip_page.query_selector_all('input[type="file"]')
        print(f"Encontrados {len(file_inputs)} file inputs")
        if file_inputs and libro_file:
            print("Subiendo manuscrito...")
            await file_inputs[0].set_input_files(str(libro_file))
            await payhip_page.wait_for_timeout(2000)

        # 2. Título
        title_el = await payhip_page.query_selector('#p_name, input[name="p_name"]')
        if title_el:
            await title_el.fill(titulo)
            print("Título llenado OK")

        # 3. Precio
        price_el = await payhip_page.query_selector('#p_price, input[name="p_price"]')
        if price_el:
            await price_el.fill(precio)
            print("Precio llenado OK")

        # 4. Portada
        if len(file_inputs) > 1 and portada.exists():
            print("Subiendo portada.jpg...")
            await file_inputs[1].set_input_files(str(portada))
            await payhip_page.wait_for_timeout(2000)

        # 5. Descripción (Quill Rich Text Editor)
        editor = await payhip_page.query_selector('.ql-editor')
        if editor:
            await editor.evaluate("(el, html) => el.innerHTML = html", desc_html)
            print("Descripción HTML llenada OK")

        print("\n¡Formulario completado en Payhip! Mirá tu navegador Brave para confirmar.")

if __name__ == "__main__":
    asyncio.run(test_fill_payhip("de-cero-a-negocio-con-ia"))
