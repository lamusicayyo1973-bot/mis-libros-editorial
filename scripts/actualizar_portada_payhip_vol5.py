# -*- coding: utf-8 -*-
import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORTADA_PATH = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5\portada.jpg")
USER_DATA_DIR = Path(r"C:\Proyectos\mis-libros-editorial\browser_session_payhip")

async def actualizar_payhip():
    async with async_playwright() as p:
        print("Lanzando navegador para actualizar portada en Payhip...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=True,
            viewport={"width": 1280, "height": 800}
        )
        page = context.pages[0] if context.pages else await context.new_page()

        print("Navegando a https://payhip.com/products...")
        await page.goto("https://payhip.com/products", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # Buscar el producto Volumen 5
        edit_link = None
        all_edits = await page.query_selector_all("a[href*='/edit/']")
        for e in all_edits:
            parent = await e.evaluate_handle("el => el.closest('tr')")
            if parent:
                p_txt = await parent.inner_text()
                if "Volumen 5" in p_txt:
                    edit_link = await e.get_attribute("href")
                    break

        if edit_link:
            if not edit_link.startswith("http"):
                edit_link = "https://payhip.com" + edit_link
            print(f"Edit link encontrado: {edit_link}")
            await page.goto(edit_link, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Subir nueva imagen de portada
            img_input = await page.query_selector("input[type='file'][accept*='image']")
            if not img_input:
                img_input = await page.query_selector("input[type='file']")

            if img_input:
                print("Cargando nueva portada en Payhip...")
                await img_input.set_input_files(str(PORTADA_PATH))
                await page.wait_for_timeout(3000)

                # Guardar producto
                save_btn = await page.query_selector("button:has-text('Save'), button[type='submit'], input[type='submit']")
                if save_btn:
                    await save_btn.click()
                    await page.wait_for_timeout(4000)
                    print("✅ [PAYHIP] Portada del Volumen 5 actualizada con exito!")
            else:
                print("No se encontro selector de imagen en Payhip.")
        else:
            print("No se encontro el producto Volumen 5 en la lista de Payhip.")

if __name__ == "__main__":
    asyncio.run(actualizar_payhip())
