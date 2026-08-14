# -*- coding: utf-8 -*-
"""
===============================================================================
HOTMART UNIFIED PUBLISHER & AUTOMATIC LOGIN SESSION
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
USER_DATA_DIR = Path(r"C:\Proyectos\mis-libros-editorial\playwright_hotmart_profile")

# Lista de libros a procesar
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

    print(f"\n--- PROCESANDO: {titulo} ---")
    await page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
    await page.wait_for_timeout(2500)

    # 1. Click en eBook
    ebook_btn = await page.wait_for_selector('button[id="4"], button:has-text("eBook")', timeout=10000)
    if ebook_btn:
        await ebook_btn.click()
        await page.wait_for_timeout(3000)

    # 2. Formulario Info
    name_in = await page.wait_for_selector('#name, input[name="name"]', timeout=10000)
    await name_in.fill(titulo)

    desc_in = await page.query_selector('#description, textarea[name="description"]')
    if desc_in:
        await desc_in.fill(desc_text)

    cat_btn = await page.query_selector(f'button:has-text("{cat_text}")')
    if not cat_btn:
        cat_btn = await page.query_selector('button:has-text("Literatura"), button:has-text("Negocios y Carrera")')
    if cat_btn:
        await cat_btn.click()

    cover_in = await page.query_selector('#cover, input[type="file"]')
    if cover_in and portada.exists():
        await cover_in.set_input_files(str(portada))
        await page.wait_for_timeout(3000)

    cont_btn1 = await page.query_selector('button:has-text("Continuar"), button[type="submit"]')
    if cont_btn1:
        await cont_btn1.click()
        await page.wait_for_timeout(4000)

    print(f"   [OK] Borrador creado para {folder_name} en {page.url}")
    return True

async def main():
    async with async_playwright() as p:
        print("Lanzando ventana visible para Hotmart...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--start-maximized"]
        )
        page = context.pages[0]
        await page.goto("https://app.hotmart.com/products")
        await page.wait_for_timeout(3000)

        # Esperar a que el usuario este logueado
        print("\n=======================================================")
        print("POR FAVOR INICIA SESION EN LA VENTANA QUE SE ABRIO.")
        print("Podes hacer clic en 'Enter with Google' o poner tu clave.")
        print("=======================================================\n")

        while "login" in page.url or "sso" in page.url:
            print("Esperando inicio de sesión en pantalla...")
            await asyncio.sleep(3)

        print("\n>>> SESION INICIADA CORRECTAMENTE EN HOTMART! <<<")
        print("Comenzando carga automatica de los 14 libros...\n")

        exitosos = 0
        for book in LIBROS:
            try:
                res = await publicar_libro(page, book)
                if res:
                    exitosos += 1
            except Exception as e:
                print(f"   [!] Error en {book}: {e}")

        print(f"\n=======================================================")
        print(f"FINALIZADO: {exitosos}/{len(LIBROS)} libros subidos a Hotmart")
        print(f"=======================================================\n")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
