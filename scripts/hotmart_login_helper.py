# -*- coding: utf-8 -*-
import sys, json, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

USER_DATA_DIR = Path(r"C:\Proyectos\mis-libros-editorial\browser_session_hotmart")
BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

EMAIL = "nicolasnoguera199@gmail.com"
PASS = "Lambi2025"

async def run_hotmart_login():
    async with async_playwright() as p:
        print("Lanzando navegador visible en pantalla...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--start-maximized"]
        )
        page = context.pages[0]
        
        print("Navegando a Hotmart Login...")
        await page.goto("https://app.hotmart.com/login", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Cookies
        cookie = await page.query_selector("button:has-text('OK'), button:has-text('Aceptar')")
        if cookie:
            try:
                await cookie.click()
                await page.wait_for_timeout(1000)
            except:
                pass

        # Email
        print("Escribiendo email...")
        email_in = await page.wait_for_selector("input[type='email'], input[name='username'], input[id='username']", timeout=10000)
        await email_in.click()
        await email_in.fill("")
        await email_in.press_sequentially(EMAIL, delay=50)

        # Password
        print("Escribiendo clave...")
        pass_in = await page.wait_for_selector("input[type='password'], input[name='password'], input[id='password']", timeout=10000)
        await pass_in.click()
        await pass_in.fill("")
        await pass_in.press_sequentially(PASS, delay=50)

        await page.wait_for_timeout(1000)
        print("Haciendo clic en el boton de ingreso...")
        submit = await page.query_selector("button[type='submit'], button:has-text('Entrar'), button:has-text('Log in')")
        if submit:
            await submit.click()

        print("Esperando 10 segundos para verificar inicio de sesion...")
        await page.wait_for_timeout(10000)

        print("URL actual:", page.url)
        if "login" not in page.url and "sso" not in page.url:
            print(">>> LOGIN EXITOSO DETECTADO. MANTENIENDO NAVEGADOR Y PROCEDIENDO. <<<")
            # Dejar abierto para la carga
            while True:
                await asyncio.sleep(1)
        else:
            print("Aun en pantalla de login/error. URL:", page.url)
            await page.screenshot(path=r"C:\Proyectos\mis-libros-editorial\login_attempt.png")

if __name__ == "__main__":
    asyncio.run(run_hotmart_login())
