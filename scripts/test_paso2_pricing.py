# -*- coding: utf-8 -*-
"""
===============================================================================
TEST PASO 2 (PRICING) Y PASO 3 (CONTENT) EN HOTMART
===============================================================================
Prueba ingresar el precio ($20 USD) en /pricing y avanzar a /content
para subir el archivo manuscrito (.docx/.pdf).
===============================================================================
"""

import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

async def test_paso2_pricing():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        print("1. URL actual:", hotmart_page.url)

        # Si no está en /pricing, ir a /pricing
        if "pricing" not in hotmart_page.url:
            await hotmart_page.goto("https://app.hotmart.com/products/add/4/pricing", wait_until="networkidle")
            await hotmart_page.wait_for_timeout(2000)

        # Inspeccionar todos los campos de texto e inputs en pricing
        js_fields = """
        () => {
            return Array.from(document.querySelectorAll('input, select, button')).map(e => ({
                tag: e.tagName,
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                placeholder: e.placeholder || '',
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : ''
            }));
        }
        """
        fields = await hotmart_page.evaluate(js_fields)
        print("\nCAMPOS EN STEP PRICING:")
        for f in fields:
            if f['id'] or f['name'] or f['placeholder'] or 'Continuar' in f['text'] or 'Guardar' in f['text']:
                print("  •", f)

        # Buscar input de precio
        price_in = await hotmart_page.query_selector('input[name="price"], #price, input[placeholder*="0"], input[type="text"]')
        if price_in:
            print("2. Llenando precio ($20)...")
            await price_in.fill("20")
            await hotmart_page.wait_for_timeout(1000)

        # Clic en Continuar
        cont_btn = await hotmart_page.query_selector('button:has-text("Continuar"), button:has-text("Guardar"), button[type="submit"]')
        if cont_btn:
            print("3. Presionando 'Continuar' en Precificación...")
            await cont_btn.click()
            await hotmart_page.wait_for_timeout(4000)

        print("4. URL FINAL DESPUES DE PRICING:", hotmart_page.url)

if __name__ == "__main__":
    asyncio.run(test_paso2_pricing())
