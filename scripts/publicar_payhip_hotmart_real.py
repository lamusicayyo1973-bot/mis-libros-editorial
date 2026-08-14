# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICADOR AUTOMATICO - PAYHIP & HOTMART (Microsoft Edge + Perfil Persistente)
===============================================================================
Autor: Alberto Nicolás Noguera

Usa Microsoft Edge (ya instalado en Windows) con un perfil dedicado y persistente.
- Primera vez: Edge abre, iniciás sesión en Payhip y Hotmart, y guarda la sesión.
- Siguientes veces: Edge abre ya logueado, completa el formulario solo.
- No hay conflicto con Chrome porque usa un navegador diferente.
===============================================================================
"""

import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(r"C:\Proyectos\mis-libros-editorial")
BOOKS_DIR = BASE_DIR / "libros"
EDGE_EXE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
EDGE_PROFILE = r"C:\Proyectos\loki\brave_editorial_profile"


async def esperar_login_y_cloudflare(page, nombre_servicio, url_destino):
    """Espera hasta 10 minutos mientras el usuario inicia sesión o Cloudflare pasa."""
    primer_aviso = True
    for i in range(300):
        try:
            url = page.url.lower()
            title = (await page.title()).lower()

            es_cloudflare = "just a moment" in title or "verifica" in title or "checking" in title
            es_login = any(k in url for k in ["login", "signin", "auth", "sso", "accounts"])
            es_destino = url_destino.lower() in url

            if es_cloudflare:
                if primer_aviso:
                    print(f"        [!] {nombre_servicio}: Cloudflare activo - hacé clic en la casilla si aparece...")
                    primer_aviso = False
                await asyncio.sleep(2)
                continue

            if es_login:
                if primer_aviso:
                    print(f"        [!] {nombre_servicio}: Iniciá sesión en la ventana de Edge...")
                    primer_aviso = False
                await asyncio.sleep(2)
                continue

            if es_destino:
                print(f"        [✓] {nombre_servicio}: Acceso confirmado.")
                return True

            await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(2)
    return False


async def autocompletar_campos(page, titulo, precio_usd, docx_file, portada_file, plataforma):
    completados = 0

    if plataforma == "payhip":
        for sel in ['input[name="title"]', '#product-title', 'input[placeholder*="title" i]']:
            el = page.locator(sel)
            if await el.count() > 0:
                await el.first.triple_click()
                await el.first.fill(titulo)
                print(f"        [✓] Título cargado")
                completados += 1
                break

        for sel in ['input[name="price"]', '#product-price', 'input[placeholder*="price" i]']:
            el = page.locator(sel)
            if await el.count() > 0:
                await el.first.triple_click()
                await el.first.fill(precio_usd)
                print(f"        [✓] Precio cargado: ${precio_usd} USD")
                completados += 1
                break

        if docx_file.exists():
            for sel in ['input[type="file"]']:
                el = page.locator(sel)
                if await el.count() > 0:
                    try:
                        await el.first.set_input_files(str(docx_file))
                        print(f"        [✓] Manuscrito adjuntado")
                        completados += 1
                    except Exception:
                        pass
                    break

    elif plataforma == "hotmart":
        for sel in ['input[name="name"]', '#product-name', 'input[placeholder*="name" i]', 'input[placeholder*="nombre" i]']:
            el = page.locator(sel)
            if await el.count() > 0:
                await el.first.triple_click()
                await el.first.fill(titulo)
                print(f"        [✓] Nombre cargado en Hotmart")
                completados += 1
                break

    if completados == 0:
        print(f"        [!] No se encontraron campos para autocompletar en {plataforma}.")
        print(f"            El formulario puede haber cambiado su diseño.")

    return completados


async def publicar_con_edge(book_id):
    book_folder = BOOKS_DIR / book_id
    ficha_file = book_folder / "ficha_producto.json"

    if not ficha_file.exists():
        print(f"[X] No existe ficha_producto.json en {book_folder}")
        input("Presiona ENTER para salir...")
        return

    with open(ficha_file, "r", encoding="utf-8") as f:
        ficha = json.load(f)

    titulo = f"{ficha.get('titulo')}: {ficha.get('subtitulo')}" if ficha.get('subtitulo') else ficha.get('titulo')
    precio_usd = str(ficha.get("precio_usd", 20.00))
    docx_file = book_folder / "libro.docx"
    portada_file = book_folder / "portada.jpg"

    print("=" * 65)
    print(f"  LOKI AUTOPUBLICADOR - PAYHIP & HOTMART (Brave)")
    print(f"  Libro : {titulo[:55]}...")
    print(f"  Precio: ${precio_usd} USD")
    print("=" * 65)

    Path(EDGE_PROFILE).mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        print("\n  [~] Abriendo Brave con perfil editorial dedicado...")

        context = await p.chromium.launch_persistent_context(
            user_data_dir=EDGE_PROFILE,
            executable_path=EDGE_EXE,
            headless=False,
            ignore_default_args=["--enable-automation"],
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-web-security"
            ],
            viewport=None
        )

        # Aplicar sigilo a TODO el contexto (afecta a TODAS las páginas incluyendo Google login)
        await context.add_init_script("""
            // Ocultar navigator.webdriver (lo que bloquea Google)
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            // Ocultar chrome.runtime de automatización
            window.chrome = { runtime: {} };
            // Simular plugins reales del navegador
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            // Simular idiomas reales
            Object.defineProperty(navigator, 'languages', { get: () => ['es-AR', 'es', 'en-US', 'en'] });
        """)

        pages = context.pages
        page_payhip = pages[0] if pages else await context.new_page()

        # ----- 1. PAYHIP -----
        print("\n  [1/2] PAYHIP - Navegando...")
        await page_payhip.goto("https://payhip.com/product/add/digital", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)

        acceso_ok = await esperar_login_y_cloudflare(page_payhip, "Payhip", "payhip.com/product/add")

        if not acceso_ok or "add/digital" not in page_payhip.url:
            await page_payhip.goto("https://payhip.com/product/add/digital", wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(3)

        await autocompletar_campos(page_payhip, titulo, precio_usd, docx_file, portada_file, "payhip")

        # ----- 2. HOTMART -----
        print("\n  [2/2] HOTMART - Navegando...")
        page_hotmart = await context.new_page()
        await Stealth().apply_stealth_async(page_hotmart)
        await page_hotmart.goto("https://app.hotmart.com/tools/products/create", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)

        acceso_ok = await esperar_login_y_cloudflare(page_hotmart, "Hotmart", "hotmart.com/tools/products/create")

        if not acceso_ok or "products/create" not in page_hotmart.url:
            await page_hotmart.goto("https://app.hotmart.com/tools/products/create", wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(3)

        await autocompletar_campos(page_hotmart, titulo, precio_usd, docx_file, portada_file, "hotmart")

        print("\n" + "=" * 65)
        print("  🎉 PROCESO COMPLETADO")
        print("  Edge permanece abierto. Revisá los formularios y publicá.")
        print("  La sesión queda guardada para la próxima vez (sin login, sin captcha).")
        print("=" * 65)

        # Mantener Edge abierto hasta que el usuario lo cierre
        try:
            while len(context.pages) > 0:
                await asyncio.sleep(1)
        except Exception:
            pass


if __name__ == "__main__":
    book = sys.argv[1] if len(sys.argv) > 1 else "el-algoritmo-personal"
    asyncio.run(publicar_con_edge(book))
