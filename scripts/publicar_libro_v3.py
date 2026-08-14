# -*- coding: utf-8 -*-
"""
Versión corregida del publicador de libros.

Qué cambia respecto a la versión anterior:
1. NUNCA arranca en modo headless cuando puede necesitar login manual.
   El modo invisible es justamente lo que rompía el login.
2. Detecta si terminó en una página de login (por URL) y para de verdad,
   pidiendo que confirmes con Enter en la consola después de loguearte
   en la ventana visible -- en vez de un sleep(20) ciego que sigue
   igual esté logueado o no.
3. Usa page.wait_for_selector() con timeout real en vez de "count() > 0
   y sigo para adelante". Si no aparece el campo, lo marca como
   FALLIDO de verdad, saca screenshot, y NO dice "OK".
4. Al final imprime un resumen honesto: qué plataforma salió bien y
   cuál no, en vez de un mensaje de éxito genérico.
5. Amazon KDP queda deshabilitado por defecto (ver nota abajo).
"""

import sys
import io
import json
import subprocess
import time
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE_BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_PROFILE = r"C:\Proyectos\loki\automation\loki_chrome_real_profile"
CDP_PORT = 9222

# Amazon KDP queda OFF por defecto: automatizar el alta de productos ahí
# puede chocar con los términos de servicio de Amazon y arriesgar la
# cuenta. Si lo querés habilitar, hacelo a conciencia y revisá primero
# los términos de KDP.
PLATAFORMAS_ACTIVAS = ["tiendanube", "payhip", "gumroad", "hotmart"]

URLS = {
    "tiendanube": "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new",
    "payhip": "https://payhip.com/product/add/digital",
    "gumroad": "https://gumroad.com/products/new",
    "hotmart": "https://app.hotmart.com/tools/products/create",
}

SELECTORES_TITULO = {
    "tiendanube": 'input[name="name"], input#product_name, input[data-store="product-name"]',
    "payhip": 'input[name="title"], input#product-title',
    "gumroad": 'input[name="name"]',
    "hotmart": 'input[name="name"], input[placeholder*="nombre" i]',
}


def asegurar_chrome_con_cdp():
    """
    Se conecta a un Chrome ya abierto con el puerto de depuración. Si no
    hay ninguno corriendo, lo abre usando TU perfil real de Chrome (el
    que ya tiene tus sesiones logueadas) en vez de un perfil vacío.
    Esto evita depender de que corras un .bat aparte antes.
    """
    import urllib.request

    try:
        urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/version", timeout=1)
        print(f"[i] Ya hay un Chrome corriendo en el puerto {CDP_PORT}, me conecto a ese.")
        return
    except Exception:
        pass

    print(f"[i] No hay Chrome en el puerto {CDP_PORT}. Abriendo uno nuevo con tu perfil real...")
    subprocess.Popen([
        CHROME_EXE,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={CHROME_PROFILE}",
    ])
    # Esperar a que el puerto de depuración responda de verdad, no un
    # sleep fijo -- así funciona igual de rápido en una PC rápida o lenta.
    for _ in range(30):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/version", timeout=1)
            print("[i] Chrome levantado y disponible.")
            return
        except Exception:
            time.sleep(1)
    raise RuntimeError(
        f"Chrome no respondió en el puerto {CDP_PORT} después de 30s. "
        "Revisá que la ruta CHROME_EXE sea correcta en este script."
    )


def parece_pagina_de_login(url: str) -> bool:
    return "login" in url or "auth" in url or "sso." in url


async def esperar_login_si_hace_falta(page, plataforma: str, timeout_segundos: int = 300):
    """
    Si terminamos en una URL de login, esperamos de verdad a que inicies
    sesión -- pero sin usar input(), que revienta con EOFError cuando el
    script corre sin consola interactiva (como lo ejecuta Antigravity).

    En vez de eso, revisamos la URL de la página cada 2 segundos: en
    cuanto deje de ser una pantalla de login (porque vos ya iniciaste
    sesión en la ventana de Chrome), seguimos solos. Si pasan
    timeout_segundos (5 minutos por defecto) sin que eso pase, lo
    marcamos como fallido en vez de quedarnos esperando para siempre.
    """
    if not parece_pagina_de_login(page.url):
        return True

    print(f"    [!] {plataforma}: hace falta loguearse.")
    print(f"        Andá a la ventana de Chrome e iniciá sesión en {plataforma}.")
    print(f"        Voy a esperar hasta {timeout_segundos}s a que termines "
          f"(no hace falta que hagas nada más acá).")

    esperado = 0
    intervalo = 2
    while esperado < timeout_segundos:
        await asyncio.sleep(intervalo)
        esperado += intervalo
        if not parece_pagina_de_login(page.url):
            print(f"        [i] Login detectado en {plataforma} después de {esperado}s.")
            await page.goto(URLS[plataforma], wait_until="domcontentloaded")
            await asyncio.sleep(1)
            return True
        if esperado % 20 == 0:
            print(f"        ... siguen esperando login en {plataforma} ({esperado}s)")

    print(f"    [FALLÓ] Pasaron {timeout_segundos}s y {plataforma} sigue en login. "
          f"Probablemente no llegaste a loguearte a tiempo.")
    return False


async def publicar_en_plataforma(page, plataforma: str, book_folder: Path, ficha: dict) -> bool:
    """Devuelve True solo si de verdad pudo completar el título. No miente."""
    titulo = ficha.get("titulo", book_folder.name)
    print(f"\n  [{plataforma.upper()}] {titulo}")

    try:
        await page.goto(URLS[plataforma], wait_until="domcontentloaded")
        logueado = await esperar_login_si_hace_falta(page, plataforma)
        if not logueado:
            return False

        selector = SELECTORES_TITULO[plataforma]
        try:
            campo = await page.wait_for_selector(selector, timeout=15000, state="visible")
        except Exception:
            screenshot_path = book_folder / f"debug_{plataforma}.png"
            await page.screenshot(path=str(screenshot_path))
            print(f"    [FALLÓ] No encontré el campo de título en {plataforma}. "
                  f"Screenshot: {screenshot_path}")
            print(f"    Posibles causas: la plataforma cambió el formulario, "
                  f"o seguimos en una página que no es la esperada (URL actual: {page.url}).")
            return False

        await campo.fill(titulo)
        print(f"    [OK] Título cargado en {plataforma}: {titulo}")
        return True

    except Exception as e:
        print(f"    [ERROR] {plataforma}: {type(e).__name__}: {e}")
        return False


async def publicar_libro(book_id: str):
    book_folder = BASE_BOOKS_DIR / book_id
    ficha_file = book_folder / "ficha_producto.json"
    if not ficha_file.exists():
        print(f"[-] No existe {ficha_file}, no puedo publicar {book_id}")
        return

    with open(ficha_file, "r", encoding="utf-8") as f:
        ficha = json.load(f)

    asegurar_chrome_con_cdp()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
        context = browser.contexts[0]
        # Importante: NUNCA reusamos una pestaña existente (context.pages[0]).
        # Si el usuario tiene ese Chrome abierto con otras pestañas -- por
        # ejemplo la del chat -- reusar la primera terminaría navegando esa
        # pestaña a los sitios de venta sin que el usuario lo note. Siempre
        # abrimos una pestaña nueva, dedicada solo a la automatización.
        page = await context.new_page()

        resultados = {}
        for plataforma in PLATAFORMAS_ACTIVAS:
            resultados[plataforma] = await publicar_en_plataforma(page, plataforma, book_folder, ficha)

        print(f"\n{'='*50}")
        print(f"RESUMEN — {ficha.get('titulo', book_id)}")
        print(f"{'='*50}")
        for plataforma, ok in resultados.items():
            estado = "OK (título cargado)" if ok else "FALLÓ"
            print(f"  {plataforma:12s}: {estado}")
        print(
            "\nNota: esto solo confirma que se cargó el TÍTULO. Todavía falta "
            "completar precio, descripción, portada y archivo, y revisar cada "
            "borrador a mano antes de publicar de verdad."
        )


if __name__ == "__main__":
    book = sys.argv[1] if len(sys.argv) > 1 else "de-cero-a-negocio-con-ia"
    asyncio.run(publicar_libro(book))
