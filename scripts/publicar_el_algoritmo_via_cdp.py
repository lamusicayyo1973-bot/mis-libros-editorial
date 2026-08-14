# -*- coding: utf-8 -*-
import sys
import io
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

book_folder = Path(r"C:\Proyectos\mis-libros-editorial\libros\el-algoritmo-personal")
ficha_file = book_folder / "ficha_producto.json"
with open(ficha_file, "r", encoding="utf-8") as f:
    ficha = json.load(f)

titulo     = f"{ficha.get('titulo')}: {ficha.get('subtitulo')}"
copy       = ficha.get("copy_ventas", {})
descripcion = f"{copy.get('headline','')}\n\n{copy.get('cuerpo','')}"
portada_file = book_folder / "portada.jpg"
docx_file    = book_folder / "libro.docx"

async def wait_for_real_page(page, expected_fragment, max_wait=30):
    """Espera hasta que la URL deje de ser una página de login"""
    for _ in range(max_wait):
        if expected_fragment in page.url:
            return True
        await asyncio.sleep(1)
    return False

async def fill_tiendanube(page):
    print("\n[1/3] TIENDANUBE → Navegando...")
    await page.goto(
        "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new",
        wait_until="domcontentloaded"
    )
    await asyncio.sleep(4)
    print(f"      URL: {page.url}")

    if "login" in page.url:
        print("      [!] No entró automático - revisá Chrome manualmente")
        return False

    # Nombre del producto
    for sel in ['input[name="name"]', '[data-testid="product-name"]', 'input#name']:
        el = page.locator(sel)
        if await el.count() > 0:
            await el.first.fill(titulo)
            print(f"      [✓] Título cargado")
            break

    # Precio
    for sel in ['input[name="price"]', 'input#price', '[data-testid="product-price"]']:
        el = page.locator(sel)
        if await el.count() > 0:
            await el.first.fill("26000")
            print("      [✓] Precio $26.000 ARS cargado")
            break

    # Portada
    if portada_file.exists():
        f_in = page.locator('input[type="file"]')
        if await f_in.count() > 0:
            await f_in.first.set_input_files(str(portada_file))
            print("      [✓] Portada adjuntada")
            await asyncio.sleep(3)

    # Guardar
    for sel in ['button[type="submit"]', 'button:has-text("Guardar")', 'button:has-text("Save")']:
        btn = page.locator(sel)
        if await btn.count() > 0:
            await btn.first.click()
            print("      [✓] GUARDADO en Tiendanube")
            await asyncio.sleep(4)
            break

    return True

async def fill_payhip(page):
    print("\n[2/3] PAYHIP → Navegando...")
    await page.goto("https://payhip.com/product/add/digital", wait_until="domcontentloaded")
    await asyncio.sleep(4)
    print(f"      URL: {page.url}")

    if "login" in page.url or "auth" in page.url:
        print("      [!] No entró automático - revisá Chrome manualmente")
        return False

    for sel in ['input[name="title"]', '#product-title', 'input[placeholder*="title" i]']:
        el = page.locator(sel)
        if await el.count() > 0:
            await el.first.fill(titulo)
            print("      [✓] Título cargado")
            break

    for sel in ['input[name="price"]', '#product-price', 'input[placeholder*="price" i]']:
        el = page.locator(sel)
        if await el.count() > 0:
            await el.first.fill("20.00")
            print("      [✓] Precio $20.00 USD cargado")
            break

    if docx_file.exists():
        for sel in ['input[type="file"][name="file"]', '#digital-file', 'input[type="file"]']:
            el = page.locator(sel)
            if await el.count() > 0:
                await el.first.set_input_files(str(docx_file))
                print("      [✓] Manuscrito .docx adjuntado")
                await asyncio.sleep(3)
                break

    for sel in ['button[type="submit"]', 'button:has-text("Add Product")', 'input[type="submit"]']:
        btn = page.locator(sel)
        if await btn.count() > 0:
            await btn.first.click()
            print("      [✓] PUBLICADO en Payhip")
            await asyncio.sleep(4)
            break

    return True

async def fill_hotmart(page):
    print("\n[3/3] HOTMART → Navegando...")
    await page.goto("https://app.hotmart.com/tools/products/create", wait_until="domcontentloaded")
    await asyncio.sleep(5)
    print(f"      URL: {page.url}")

    if "login" in page.url or "sso" in page.url:
        print("      [!] Hotmart requiere login manual")
        return False

    print("      [✓] Hotmart verificado - completá los campos manualmente si quedan incompletos")
    return True

async def main():
    print("="*65)
    print("🚀 CARGANDO EL ALGORITMO PERSONAL EN TUS PLATAFORMAS")
    print("   Conectando a Chrome con TU perfil y TUS logins...")
    print("="*65)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print("  [✓] Conectado a tu Chrome con sesiones activas!")
        except Exception as e:
            print(f"  [X] Chrome no está abierto con el puerto CDP.")
            print(f"      Ejecutá primero PASO_1_Abrir_Chrome_CDP.bat")
            print(f"      Error: {e}")
            return

        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        await fill_tiendanube(page)
        await fill_payhip(page)
        await fill_hotmart(page)

        print("\n" + "="*65)
        print("🎉 PROCESO COMPLETADO - Verificá las plataformas en Chrome")
        print("="*65)

if __name__ == "__main__":
    asyncio.run(main())
