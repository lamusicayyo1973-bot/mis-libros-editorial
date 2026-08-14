# -*- coding: utf-8 -*-
"""
===============================================================================
HOTMART AUTO-PUBLISHER FOR ACTIVE PORT 9222 SESSION
===============================================================================
"""
import sys, json, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

LIBROS = [
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
    "oni-no-ketsuryu-volumen-10"
]

async def publicar_libro(page, folder_name):
    folder_path = BOOKS_DIR / folder_name
    ficha_file = folder_path / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"   [!] Ficha no encontrada para {folder_name}")
        return False

    with open(ficha_file, encoding="utf-8") as f:
        ficha = json.load(f)

    titulo = ficha.get("titulo", folder_name)[:100]
    desc_base = ficha.get("descripcion", "") or ficha.get("headline", "")
    beneficios = " ".join(ficha.get("beneficios", []))
    capitulos = " ".join(ficha.get("capitulos", []))
    desc_text = f"{desc_base}\n\nLo que incluye este eBook:\n{beneficios}\n\nContenido:\n{capitulos}\n\nEdición oficial de Nicolás Noguera Editorial. Formato digital."
    
    portada = folder_path / "portada.jpg"
    cat_text = "Literatura" if "kuro" in folder_name or "oni" in folder_name else "Negocios y Carrera"

    print(f"\n========================================================")
    print(f" SUBIENDO EN VIVO: {titulo}")
    print(f"========================================================")
    
    await page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    # 1. Click en eBook
    ebook_btn = await page.wait_for_selector('button[id="4"], button:has-text("eBook")', timeout=15000)
    if ebook_btn:
        print(" -> Clickeando botón eBook...")
        await ebook_btn.click()
        await page.wait_for_timeout(3000)

    # 2. Formulario Info
    print(" -> Cargando título y descripción...")
    name_in = await page.wait_for_selector('#name, input[name="name"]', timeout=15000)
    await name_in.fill(titulo)

    desc_in = await page.query_selector('#description, textarea[name="description"]')
    if desc_in:
        await desc_in.fill(desc_text)

    cat_btn = await page.query_selector(f'button:has-text("{cat_text}")')
    if not cat_btn:
        cat_btn = await page.query_selector('button:has-text("Literatura"), button:has-text("Negocios y Carrera")')
    if cat_btn:
        await cat_btn.click()
        print(f" -> Categoría ({cat_text}) seleccionada.")

    cover_in = await page.query_selector('#cover, input[type="file"]')
    if cover_in and portada.exists():
        await cover_in.set_input_files(str(portada))
        print(" -> Portada cargada.")
        await page.wait_for_timeout(3000)

    cont_btn1 = await page.query_selector('button:has-text("Continuar"), button[type="submit"]')
    if cont_btn1:
        print(" -> Avanzando a Precificación...")
        await cont_btn1.click()
        await page.wait_for_timeout(5000)

    print(f" [OK] Borrador guardado exitosamente para {folder_name}!")
    return True

async def main():
    async with async_playwright() as p:
        print("Conectando a Brave (puerto 9222)...")
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        print("Esperando a que la URL este en el panel de Hotmart...")
        while "login" in page.url or "sso" in page.url:
            print("  -> Aguardando inicio de sesion (hacer clic en Enter with Google en el navegador)...")
            await asyncio.sleep(4)

        print("\n>>> ¡SESION DETECTADA EN HOTMART! INICIANDO CARGA AUTOMATICA DE LIBROS <<<\n")
        
        exitosos = 0
        for book in LIBROS:
            try:
                res = await publicar_libro(page, book)
                if res:
                    exitosos += 1
            except Exception as e:
                print(f" [!] Error en {book}: {e}")

        print(f"\n=======================================================")
        print(f" PROCESO FINALIZADO: {exitosos}/{len(LIBROS)} libros subidos a Hotmart")
        print(f"=======================================================\n")

if __name__ == "__main__":
    asyncio.run(main())
