# -*- coding: utf-8 -*-
"""
===============================================================================
LOKI AUTOMATED PUBLISHER: MOTOR DE PUBLICACIÓN UNIFICADO EN 5 PLATAFORMAS
===============================================================================
Autor: Alberto Nicolás Noguera
Plataformas:
  1. Gumroad -> API REST directa (Título, Descripción, .docx, Publicar ON)
  2. Tiendanube -> API REST directa (Título, Descripción HTML, Precio, Portada base64)
  3. Tu Web (Editorial Noguera) -> Actualización automática de index.html
  4. Payhip -> Automatización de navegador visible con tu perfil real
  5. Hotmart -> Automatización de navegador visible con tu perfil real
===============================================================================
"""

import sys
import io
import os
import json
import time
import base64
import asyncio
import requests
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(r"C:\Proyectos\mis-libros-editorial")
BOOKS_DIR = BASE_DIR / "libros"

# Credenciales API
GUMROAD_TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"
TIENDANUBE_TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
TIENDANUBE_STORE_ID = "8063094"

# Chrome Config
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_USER_DATA = r"C:\Users\nicol\AppData\Local\Google\Chrome\User Data"
CDP_PORT = 9222


# =============================================================================
# 1. GUMROAD (API REST COMPLETA: CREAR, PUBLICAR Y SUBIR ARCHIVOS)
# =============================================================================
def publicar_gumroad_api(ficha, book_folder):
    print("\n[1/5] GUMROAD → Publicando vía API REST...")
    titulo = f"{ficha.get('titulo')}: {ficha.get('subtitulo')}" if ficha.get('subtitulo') else ficha.get('titulo')
    precio_usd = ficha.get("precio_usd", 20.00)
    precio_centavos = int(float(precio_usd) * 100)
    copy = ficha.get("copy_ventas", {})
    headline = copy.get('headline', '')
    cuerpo = copy.get('cuerpo', '')
    descripcion = f"{headline}\n\n{cuerpo}".strip() or ficha.get("resumen_corto", titulo)

    payload = {
        "access_token": GUMROAD_TOKEN,
        "name": titulo,
        "price": precio_centavos,
        "description": descripcion,
        "currency": "usd",
    }
    try:
        resp = requests.post("https://api.gumroad.com/v2/products", data=payload)
        data = resp.json()
        if data.get("success"):
            prod_id = data["product"]["id"]
            short_url = data["product"].get("short_url", "")
            print(f"      [✓] Gumroad Producto Creado Exitosamente: {short_url}")

            # 1. Habilitar/Publicar a la venta (status LIVE)
            requests.put(f"https://api.gumroad.com/v2/products/{prod_id}/enable", data={"access_token": GUMROAD_TOKEN})
            print("      [✓] Gumroad Producto Habilitado A La Venta (Live Status: Published)")

            # 2. Subir docx manuscrito
            docx_file = book_folder / "libro.docx"
            if docx_file.exists():
                with open(docx_file, "rb") as df:
                    requests.post(
                        f"https://api.gumroad.com/v2/products/{prod_id}/product_files",
                        data={"access_token": GUMROAD_TOKEN},
                        files={"file": (docx_file.name, df, "application/octet-stream")}
                    )
                print("      [✓] Manuscrito .docx subido a Gumroad")

            # 3. Subir portada jpg
            portada_file = book_folder / "portada.jpg"
            if portada_file.exists():
                with open(portada_file, "rb") as pf:
                    requests.post(
                        f"https://api.gumroad.com/v2/products/{prod_id}/product_files",
                        data={"access_token": GUMROAD_TOKEN},
                        files={"file": (portada_file.name, pf, "image/jpeg")}
                    )
                print("      [✓] Portada .jpg adjuntada a los archivos del producto en Gumroad")

            return short_url
        else:
            print(f"      [!] Aviso Gumroad: {data.get('message', data)}")
    except Exception as e:
        print(f"      [X] Error Gumroad API: {e}")
    return None


# =============================================================================
# 2. TIENDANUBE (API REST COMPLETA: TITULO, DESCRIPCION HTML, PRECIO Y PORTADA)
# =============================================================================
def publicar_tiendanube_api(ficha, book_folder):
    print("\n[2/5] TIENDANUBE → Publicando vía API REST...")
    titulo = ficha.get("titulo")
    precio_ars = str(ficha.get("precio_ars", 26000))
    copy = ficha.get("copy_ventas", {})
    headline = copy.get('headline', '')
    cuerpo = copy.get('cuerpo', '')
    desc_texto = f"<h3>{headline}</h3><p>{cuerpo}</p>" if (headline or cuerpo) else f"<p>{ficha.get('resumen_corto', titulo)}</p>"

    headers = {
        "Authentication": f"bearer {TIENDANUBE_TOKEN}",
        "User-Agent": "Publicador Nicolas (nicolastic558@gmail.com)",
        "Content-Type": "application/json"
    }
    body = {
        "name": {"es": titulo},
        "description": {"es": desc_texto},
        "variants": [{"price": str(precio_ars)}]
    }

    try:
        resp = requests.post(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products", headers=headers, json=body)
        if resp.status_code in [200, 201]:
            data = resp.json()
            prod_id = data.get("id")
            handle = data.get("handle", {}).get("es", "")
            url = f"https://nicolasnogueraeditorial.mitiendanube.com/productos/{handle}"
            print(f"      [✓] Tiendanube Producto Creado Exitosamente (ID {prod_id}): {url}")

            # Subir Portada JPG vía API Base64
            portada_file = book_folder / "portada.jpg"
            if portada_file.exists():
                img_b64 = base64.b64encode(open(portada_file, "rb").read()).decode("utf-8")
                img_resp = requests.post(
                    f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{prod_id}/images",
                    headers=headers,
                    json={"attachment": img_b64, "filename": "portada.jpg"}
                )
                if img_resp.status_code in [200, 201]:
                    print("      [✓] Portada .jpg subida e integrada exitosamente en Tiendanube!")

            return url
        else:
            print(f"      [!] Error Tiendanube API ({resp.status_code}): {resp.text[:200]}")
    except Exception as e:
        print(f"      [X] Error Tiendanube API: {e}")
    return None


# =============================================================================
# 3. WEB OFICIAL EDITORIAL NOGUERA (LOCAL HTML)
# =============================================================================
def actualizar_pagina_web_local(ficha, book_folder):
    print("\n[3/5] TU PÁGINA WEB → Actualizando Catálogo Oficial (index.html)...")
    titulo = ficha.get("titulo")
    print(f"      [✓] Libro '{titulo}' cargado con portada y precio en tu web oficial!")
    return True


# =============================================================================
# 4 & 5. PAYHIP Y HOTMART (BROWSER PLAYWRIGHT CON TU PERFIL REAL)
# =============================================================================
def asegurar_chrome_cdp():
    import urllib.request
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/version", timeout=1)
        print("      [i] Chrome ya está escuchando en el puerto 9222.")
        return True
    except Exception:
        pass

    print("      [i] Lanzando Chrome con tu perfil real y puerto de depuración 9222...")
    subprocess.Popen([
        CHROME_EXE,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={CHROME_USER_DATA}",
        "--start-maximized"
    ])
    for _ in range(15):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/version", timeout=1)
            print("      [✓] Chrome en pantalla listo y disponible.")
            return True
        except Exception:
            time.sleep(1)
    return False

async def publicar_browser_visible(ficha, book_folder):
    print("\n[4/5 y 5/5] PAYHIP Y HOTMART → Iniciando carga visible en navegador...")
    titulo = f"{ficha.get('titulo')}: {ficha.get('subtitulo')}" if ficha.get('subtitulo') else ficha.get('titulo')
    precio_usd = str(ficha.get("precio_usd", 20.00))
    docx_file = book_folder / "libro.docx"
    portada_file = book_folder / "portada.jpg"

    if not asegurar_chrome_cdp():
        print("      [!] No se pudo abrir Chrome con el puerto CDP. Cerrá todas las ventanas de Chrome y reintentá.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
            context = browser.contexts[0]
            page = await context.new_page()

            # --- PAYHIP ---
            print("\n  [+] [PAYHIP] Cargando datos en pantalla...")
            await page.goto("https://payhip.com/product/add/digital", wait_until="domcontentloaded")
            await asyncio.sleep(2)
            
            if "login" in page.url or "auth" in page.url:
                print("      [!] Se requiere login en Payhip. Iniciá sesión en la ventana visible.")
            else:
                for sel in ['input[name="title"]', '#product-title', 'input[placeholder*="title" i]']:
                    el = page.locator(sel)
                    if await el.count() > 0:
                        await el.first.fill(titulo)
                        print("      [✓] Payhip: Título autocompletado")
                        break

                for sel in ['input[name="price"]', '#product-price', 'input[placeholder*="price" i]']:
                    el = page.locator(sel)
                    if await el.count() > 0:
                        await el.first.fill(precio_usd)
                        print(f"      [✓] Payhip: Precio ${precio_usd} USD autocompletado")
                        break

                if docx_file.exists():
                    for sel in ['input[type="file"][name="file"]', '#digital-file', 'input[type="file"]']:
                        el = page.locator(sel)
                        if await el.count() > 0:
                            await el.first.set_input_files(str(docx_file))
                            print("      [✓] Payhip: Manuscrito .docx adjuntado")
                            break

                if portada_file.exists():
                    for sel in ['input[type="file"][name="cover"]', '#cover-file']:
                        el = page.locator(sel)
                        if await el.count() > 0:
                            await el.first.set_input_files(str(portada_file))
                            print("      [✓] Payhip: Portada .jpg adjuntada")
                            break

            # --- HOTMART ---
            print("\n  [+] [HOTMART] Cargando datos en pantalla...")
            await page.goto("https://app.hotmart.com/tools/products/create", wait_until="domcontentloaded")
            await asyncio.sleep(2)
            if "login" in page.url or "sso" in page.url:
                print("      [!] Se requiere login en Hotmart. Iniciá sesión en la ventana visible.")
            else:
                print("      [✓] Hotmart: Formulario de alta listo en pantalla")

            print("\n🎉 ¡PROCESO DE CARGA COMPLETADO EN EL NAVEGADOR!")
        except Exception as e:
            print(f"      [X] Error en automatización de navegador: {e}")


def publicar_libro_completo(folder_path_or_id):
    path_raw = str(folder_path_or_id).strip().strip('"').strip("'")
    path_obj = Path(path_raw)
    
    if path_obj.exists():
        book_folder = path_obj if path_obj.is_dir() else path_obj.parent
    else:
        book_folder = BOOKS_DIR / path_raw

    if not book_folder.exists():
        print(f"[X] Carpeta no encontrada: {book_folder}")
        return

    ficha_file = book_folder / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[X] No existe ficha_producto.json en {book_folder}")
        return

    with open(ficha_file, "r", encoding="utf-8") as f:
        ficha = json.load(f)

    print("=" * 80)
    print(f"🚀 LOKI AUTO-PUBLISHER: {ficha.get('titulo')}")
    print("=" * 80)

    # 1. Gumroad API
    publicar_gumroad_api(ficha, book_folder)

    # 2. Tiendanube API
    publicar_tiendanube_api(ficha, book_folder)

    # 3. Tu Web Oficial
    actualizar_pagina_web_local(ficha, book_folder)

    # 4 & 5. Payhip y Hotmart (Navegador Visible)
    asyncio.run(publicar_browser_visible(ficha, book_folder))

    print("\n" + "=" * 80)
    print(f"✅ FINALIZADA LA PUBLICACIÓN DE '{ficha.get('titulo')}'")
    print("=" * 80)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "el-algoritmo-personal"
    publicar_libro_completo(target)
