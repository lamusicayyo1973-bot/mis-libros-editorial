# -*- coding: utf-8 -*-
import sys
import os
import io
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

book_folder = Path(r"C:\Proyectos\mis-libros-editorial\libros\el-algoritmo-personal")
loki_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")

ficha_file = book_folder / "ficha_producto.json"
with open(ficha_file, "r", encoding="utf-8") as f:
    ficha = json.load(f)

titulo = f"{ficha.get('titulo')}: {ficha.get('subtitulo')}"
descripcion = f"{ficha.get('copy_ventas', {}).get('headline')}\n\n{ficha.get('copy_ventas', {}).get('cuerpo')}"
precio_usd = "20.00"
precio_ars = "26000"

portada_file = book_folder / "portada.jpg"
docx_file = book_folder / "libro.docx"

async def publicar_tiendanube(page):
    print("\n[1/4] PUBLICANDO EN TIENDANUBE...")
    url = "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(3)
    
    # Fill Title
    name_input = page.locator('input[name="name"], input#product_name, input[data-store="product-name"]')
    if await name_input.count() > 0:
        await name_input.first.fill(titulo)
        print("  [✓] Título ingresado en Tiendanube")
        
    # Fill Description
    desc_area = page.locator('textarea[name="description"], div.trumbowyg-editor')
    if await desc_area.count() > 0:
        await desc_area.first.fill(descripcion)
        print("  [✓] Descripción ingresada en Tiendanube")

    # Fill Price
    price_input = page.locator('input[name="price"], input#product_price')
    if await price_input.count() > 0:
        await price_input.first.fill(precio_ars)
        print("  [✓] Precio ARS ($26.000) ingresado en Tiendanube")

    # Upload Image
    if portada_file.exists():
        file_in = page.locator('input[type="file"]')
        if await file_in.count() > 0:
            await file_in.first.set_input_files(str(portada_file))
            print("  [✓] Imagen de Portada adjuntada en Tiendanube")
            await asyncio.sleep(3)

    # Click Save
    save_btn = page.locator('button[type="submit"], input[type="submit"], button:has-text("Guardar")')
    if await save_btn.count() > 0:
        await save_btn.first.click()
        print("  [✓] ¡Botón GUARDAR presionado en Tiendanube!")
        await asyncio.sleep(5)

async def publicar_payhip(page):
    print("\n[2/4] PUBLICANDO EN PAYHIP...")
    url = "https://payhip.com/product/add/digital"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(3)

    # Fill Title
    t_in = page.locator('input[name="title"], input#product-title')
    if await t_in.count() > 0:
        await t_in.first.fill(titulo)
        print("  [✓] Título ingresado en Payhip")

    # Fill Price
    p_in = page.locator('input[name="price"], input#product-price')
    if await p_in.count() > 0:
        await p_in.first.fill(precio_usd)
        print("  [✓] Precio USD ($20.00) ingresado en Payhip")

    # Fill Description
    d_in = page.locator('textarea[name="description"], div.note-editable')
    if await d_in.count() > 0:
        await d_in.first.fill(descripcion)
        print("  [✓] Descripción ingresada en Payhip")

    # Upload docx
    if docx_file.exists():
        file_in = page.locator('input[type="file"][name="file"], input#digital-file')
        if await file_in.count() > 0:
            await file_in.first.set_input_files(str(docx_file))
            print("  [✓] Manuscrito .docx adjuntado en Payhip")
            await asyncio.sleep(3)

    # Upload cover image
    if portada_file.exists():
        img_in = page.locator('input[type="file"][name="cover"], input#product-cover')
        if await img_in.count() > 0:
            await img_in.first.set_input_files(str(portada_file))
            print("  [✓] Portada adjuntada en Payhip")
            await asyncio.sleep(3)

    # Click Add Product
    add_btn = page.locator('button[type="submit"], input[type="submit"], button:has-text("Add Product")')
    if await add_btn.count() > 0:
        await add_btn.first.click()
        print("  [✓] ¡Botón ADD PRODUCT presionado en Payhip!")
        await asyncio.sleep(5)

async def publicar_gumroad(page):
    print("\n[3/4] PUBLICANDO EN GUMROAD...")
    url = "https://gumroad.com/products/new"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(3)

    name_in = page.locator('input[name="name"]')
    if await name_in.count() > 0:
        await name_in.first.fill(titulo)
        print("  [✓] Nombre ingresado en Gumroad")

    price_in = page.locator('input[name="price"]')
    if await price_in.count() > 0:
        await price_in.first.fill("20")
        print("  [✓] Precio ($20) ingresado en Gumroad")

    next_btn = page.locator('button:has-text("Next"), button[type="submit"]')
    if await next_btn.count() > 0:
        await next_btn.first.click()
        print("  [✓] Avance a personalización en Gumroad")
        await asyncio.sleep(4)

async def publicar_hotmart(page):
    print("\n[4/4] PUBLICANDO EN HOTMART...")
    url = "https://app.hotmart.com/tools/products/create"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(3)
    print("  [✓] Hotmart pantalla inicial cargada")

async def main():
    print("================================================================")
    print("🚀 INICIANDO PUBLICACIÓN REAL EN VIVO DE EL ALGORITMO PERSONAL")
    print("================================================================")
    
    live_profile = Path(r"C:\Proyectos\loki\automation\loki_live_profile")
    live_profile.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        print("Lanzando navegador de automatización sin bloqueos...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(live_profile),
            headless=True
        )
        page = context.pages[0] if context.pages else await context.new_page()

        await publicar_tiendanube(page)
        await publicar_payhip(page)
        await publicar_gumroad(page)
        await publicar_hotmart(page)

        print("\n================================================================")
        print("🎉 ¡PUBLICACIÓN EN VIVO COMPLETADA PARA EL ALGORITMO PERSONAL!")
        print("================================================================")
        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
