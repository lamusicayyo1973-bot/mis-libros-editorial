# -*- coding: utf-8 -*-
"""
===============================================================================
TEST DE SELECCIÓN DE MONEDA Y PRECIO EN HOTMART (PASO 2)
===============================================================================
Abre el dropdown de Moneda, selecciona 'Dólar estadounidense', llena $20 USD,
y hace clic en 'Guardar y continuar'.
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

async def test_moneda_hotmart():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        if "pricing" not in hotmart_page.url:
            await hotmart_page.goto("https://app.hotmart.com/products/add/4/pricing", wait_until="networkidle")
            await hotmart_page.wait_for_timeout(2000)

        print("1. Clickeando en el selector de Moneda...")
        moneda_trigger = await hotmart_page.query_selector('.hot-form, [class*="select"], [class*="input"]')
        if moneda_trigger:
            await moneda_trigger.click()
            await hotmart_page.wait_for_timeout(1000)

        print("2. Seleccionando 'Dólar estadounidense'...")
        usd_option = await hotmart_page.query_selector('div:has-text("Dólar estadounidense"), span:has-text("Dólar estadounidense"), li:has-text("Dólar estadounidense")')
        if usd_option:
            await usd_option.click()
            await hotmart_page.wait_for_timeout(1500)
            print("   -> Moneda seleccionada OK.")

        # Llenar precio $20 USD
        price_in = await hotmart_page.query_selector('input[type="text"], input[name="price"], #price')
        if price_in:
            await price_in.fill("20.00")
            print("   -> Precio $20.00 ingresado.")

        # Clic en Guardar y continuar
        save_btn = await hotmart_page.query_selector('button:has-text("Guardar y continuar"), button:has-text("Continuar")')
        if save_btn:
            print("3. Presionando 'Guardar y continuar'...")
            await save_btn.click()
            await hotmart_page.wait_for_timeout(4000)

        print("4. URL FINAL PASO 2:", hotmart_page.url)

if __name__ == "__main__":
    asyncio.run(test_moneda_hotmart())
