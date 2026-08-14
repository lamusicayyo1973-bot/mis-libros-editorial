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

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=True,
            viewport={"width": 1280, "height": 800}
        )
        page = context.pages[0] if context.pages else await context.new_page()

        print("Navegando a https://payhip.com/products...")
        await page.goto("https://payhip.com/products", wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)

        # Capturar todos los links de edicion o productos
        js_find = """
        () => {
            const links = Array.from(document.querySelectorAll('a'));
            return links.map(l => ({
                text: l.innerText.trim(),
                href: l.href,
                parentText: l.parentElement ? l.parentElement.innerText.trim() : ''
            })).filter(x => x.href.includes('/edit') || x.text.includes('Volumen') || x.parentText.includes('Volumen'));
        }
        """
        found = await page.evaluate(js_find)
        print(f"Total elementos encontrados: {len(found)}")
        
        target_link = None
        for item in found:
            print(f" -> [{item['text']}] href: {item['href']}")
            if ("Volumen 5" in item['text'] or "Volumen 5" in item['parentText']) and "/edit" in item['href']:
                target_link = item['href']
                break

        if not target_link:
            # Buscar cualquier edit link si hay lista
            for item in found:
                if "/edit" in item['href']:
                    # Inspeccionar producto
                    await page.goto(item['href'], wait_until="domcontentloaded")
                    await page.wait_for_timeout(2500)
                    body_txt = await page.inner_text("body")
                    if "Volumen 5" in body_txt:
                        target_link = item['href']
                        break

        if target_link:
            print(f"\nNavegando al link de edicion del Vol 5: {target_link}")
            await page.goto(target_link, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Subir portada
            file_input = await page.query_selector("input[type='file']")
            if file_input:
                print("Subiendo nueva portada...")
                await file_input.set_input_files(str(PORTADA_PATH))
                await page.wait_for_timeout(4000)

                # Guardar cambios
                submit_btn = await page.query_selector("button[type='submit'], input[type='submit'], button:has-text('Save')")
                if submit_btn:
                    await submit_btn.click()
                    await page.wait_for_timeout(5000)
                    print("✅ [PAYHIP] Portada del Volumen 5 actualizada con exito!")
            else:
                print("No se encontro selector de archivo en la pagina de edicion.")
        else:
            print("No se pudo localizar la URL de edicion para Volumen 5 en Payhip.")
            await page.screenshot(path=r"C:\Proyectos\mis-libros-editorial\payhip_products_debug.png")

if __name__ == "__main__":
    asyncio.run(main())
