# -*- coding: utf-8 -*-
"""
===============================================================================
DIAGNOSTICO PROFUNDO DE FORMULARIO HOTMART
===============================================================================
Abre 'https://app.hotmart.com/products/add' y analiza qué pasa exactamente
al hacer clic en los botones del formulario (errores de validación, campos
obligatorios faltantes como categoría o idioma).
===============================================================================
"""

import sys
import asyncio
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

async def diagnosticar_hotmart():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        print("1. Navegando a https://app.hotmart.com/products/add...")
        await hotmart_page.goto("https://app.hotmart.com/products/add", wait_until="networkidle")
        await hotmart_page.wait_for_timeout(2000)

        # Clic en eBook
        print("2. Haciendo clic en eBook (id=4)...")
        ebook_btn = await hotmart_page.query_selector('button[id="4"], button:has-text("eBook")')
        if ebook_btn:
            await ebook_btn.click()
            await hotmart_page.wait_for_timeout(3000)

        print("3. URL actual:", hotmart_page.url)

        # Llenar Nombre y Descripción de prueba
        name_in = await hotmart_page.query_selector('#name, input[name="name"]')
        if name_in:
            await name_in.fill("PRUEBA TEST AUTOMATION")

        desc_in = await hotmart_page.query_selector('#description, textarea[name="description"]')
        if desc_in:
            await desc_in.fill("Esta es una descripcion de prueba para verificar guardado.")

        await hotmart_page.wait_for_timeout(1000)

        # Intentar clic en Continuar
        cont_btn = await hotmart_page.query_selector('button:has-text("Continuar"), button[type="submit"]')
        if cont_btn:
            print("4. Clickeando 'Continuar'...")
            await cont_btn.click()
            await hotmart_page.wait_for_timeout(3000)

        print("5. URL después de Continuar:", hotmart_page.url)

        # Extraer mensajes de error o alertas si los hay
        js_errors = """
        () => {
            return Array.from(document.querySelectorAll('.error, [class*="error"], [class*="invalid"], .feedback, .helper-text')).map(e => e.innerText.trim()).filter(t => t.length > 0);
        }
        """
        errs = await hotmart_page.evaluate(js_errors)
        print("ALERTAS/ERRORES EN PANTALLA:", errs)

if __name__ == "__main__":
    asyncio.run(diagnosticar_hotmart())
