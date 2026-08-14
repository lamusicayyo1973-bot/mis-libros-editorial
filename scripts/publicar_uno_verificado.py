# -*- coding: utf-8 -*-
import sys, json, time, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

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

async def publicar_un_libro_directo(folder_name):
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
    print(f"  PUBLICANDO UNICO LIBRO: {titulo}")
    print(f"========================================================")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if 'payhip.com' in pg.url][0]

        await payhip_page.goto('https://payhip.com/product/add/digital', wait_until='networkidle')
        await payhip_page.wait_for_timeout(1500)

        # 1. Manuscrito (.docx/.pdf)
        file_inputs = await payhip_page.query_selector_all('input[type="file"]')
        if file_inputs and libro_file:
            print(f"  [1/4] Cargando archivo manuscrito: {libro_file.name}")
            await file_inputs[0].set_input_files(str(libro_file))
            await payhip_page.wait_for_timeout(3000)

        # 2. Título & Precio
        title_el = await payhip_page.query_selector('#p_name, input[name="p_name"]')
        if title_el:
            await title_el.fill(titulo)
            print("  [2/4] Título ingresado")

        price_el = await payhip_page.query_selector('#p_price, input[name="p_price"]')
        if price_el:
            await price_el.fill(precio)
            print(f"  [2/4] Precio ingresado: ${precio} USD")

        # 3. Portada
        if len(file_inputs) > 1 and portada.exists():
            print("  [3/4] Cargando portada.jpg...")
            await file_inputs[1].set_input_files(str(portada))
            await payhip_page.wait_for_timeout(3000)

        # 4. Descripción
        editor = await payhip_page.query_selector('.ql-editor')
        if editor:
            await editor.evaluate("(el, html) => el.innerHTML = html", desc_html)
            print("  [4/4] Descripción HTML cargada")

        # 5. Clic en #addsubmit
        print("\n  -> Clic en botón #addsubmit para Guardar y Publicar...")
        submit_btn = await payhip_page.query_selector('#addsubmit')
        if submit_btn:
            await submit_btn.click()
            await payhip_page.wait_for_timeout(5000)

        # 6. Ir a la lista de productos y mostrar confirmación
        await payhip_page.goto('https://payhip.com/products', wait_until='networkidle')
        await payhip_page.wait_for_timeout(2000)

        js = """
        () => {
            return Array.from(document.querySelectorAll('a[href*="/b/"]')).map(e => ({
                titulo: e.innerText.trim(),
                url: e.href
            }));
        }
        """
        prods = await payhip_page.evaluate(js)
        print("\n========================================================")
        print("  PRODUCTOS CONFIRMADOS PUBLICADOS EN PAYHIP:")
        for idx, pr in enumerate(prods, 1):
            print(f"   {idx}. {pr['titulo']} -> {pr['url']}")
        print("========================================================")

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "kuro-no-kineki-volumen-1"
    asyncio.run(publicar_un_libro_directo(folder))
