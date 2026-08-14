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

async def test_direct_login():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        print("Navegando a https://app.hotmart.com/login ...")
        await page.goto("https://app.hotmart.com/login", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Tratar de clickear OK de cookies
        try:
            ok_btn = await page.query_selector("button:has-text('OK'), button:has-text('Aceptar')")
            if ok_btn:
                await ok_btn.click()
                print("Cookies OK")
                await page.wait_for_timeout(1000)
        except Exception as e:
            print("Cookie note:", e)

        # Llenar email
        email_el = await page.wait_for_selector("input[type='email'], input[name='username']", timeout=10000)
        if email_el:
            await email_el.click()
            await email_el.fill(EMAIL)
            print("Email cargado OK")

        # Llenar password
        pass_el = await page.wait_for_selector("input[type='password']", timeout=10000)
        if pass_el:
            await pass_el.click()
            await pass_el.fill(PASS)
            print("Password cargada OK")

        await page.wait_for_timeout(1000)
        submit_btn = await page.query_selector("button[type='submit'], button:has-text('Log in'), button:has-text('Entrar')")
        if submit_btn:
            print("Clickeando Submit...")
            await submit_btn.click()
            await page.wait_for_timeout(8000)

        print("URL RESULTANTE:", page.url)
        title = await page.title()
        print("TITULO RESULTANTE:", title)
        await page.screenshot(path=r"C:\Proyectos\mis-libros-editorial\screenshot_login_directo.png")

if __name__ == "__main__":
    asyncio.run(test_direct_login())
