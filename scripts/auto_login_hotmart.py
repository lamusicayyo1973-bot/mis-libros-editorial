# -*- coding: utf-8 -*-
import sys, asyncio
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

EMAIL = "nicolasnoguera199@gmail.com"
PASS = "Lambi2025"

async def auto_login():
    async with async_playwright() as p:
        print("Conectando a Brave en http://localhost:9222...")
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        print("Navegando a https://app.hotmart.com/login...")
        await page.goto("https://app.hotmart.com/login", wait_until="networkidle")
        await page.wait_for_timeout(2500)

        print("Verificando si estamos en login...")
        if "login" in page.url:
            # Aceptar cookies si esta el boton
            cookie_btn = await page.query_selector("button:has-text('OK'), button:has-text('Aceptar')")
            if cookie_btn:
                try:
                    await cookie_btn.click()
                    print("Cookies aceptadas.")
                    await page.wait_for_timeout(1000)
                except Exception as e:
                    print("Cookie click warn:", e)

            # Buscar campo email / usuario
            email_input = await page.wait_for_selector("input[type='email'], input[name='username'], input[id='username'], input[placeholder*='email']", timeout=10000)
            if email_input:
                await email_input.fill(EMAIL)
                print("Email ingresado OK.")

            # Buscar campo password
            pass_input = await page.wait_for_selector("input[type='password'], input[name='password'], input[id='password']", timeout=10000)
            if pass_input:
                await pass_input.fill(PASS)
                print("Password ingresado OK.")

            # Boton entrar / submit
            submit_btn = await page.query_selector("button[type='submit'], button:has-text('Entrar'), button:has-text('Log in')")
            if submit_btn:
                print("Haciendo clic en Entrar...")
                await submit_btn.click()
                await page.wait_for_timeout(5000)

        print("URL final tras intento de login:", page.url)
        title = await page.title()
        print("Titulo final:", title)
        await page.screenshot(path=r"C:\Proyectos\mis-libros-editorial\screenshot_post_login.png")
        print("Screenshot guardado en screenshot_post_login.png.")

if __name__ == "__main__":
    asyncio.run(auto_login())
