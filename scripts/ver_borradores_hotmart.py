# -*- coding: utf-8 -*-
"""
===============================================================================
INSPECCIONAR Y CAMBIAR A PESTAÑA 'BORRADORES' O 'SOY PRODUCTOR' EN HOTMART
===============================================================================
Muestra cómo filtrar en la interfaz de Hotmart para ver todos los borradores.
===============================================================================
"""

import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        await page.goto("https://app.hotmart.com/products", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Buscar pestañas o filtros: 'Borradores', 'En aprobación', 'Soy Productor(a)', 'Todos'
        filters = await page.query_selector_all('button, a, span, tab')
        print("FILTROS Y PESTAÑAS DISPONIBLES EN HOTMART:")
        for f in filters:
            txt = (await f.inner_text()).strip().replace('\n', ' ')
            if any(k in txt.lower() for k in ['borrador', 'productor', 'todos', 'aprobacion', 'filtro', 'estado']):
                print(f"  • Elemento: '{txt}'")

        # Clic en Borradores o Todos
        draft_btn = await page.query_selector('text="Borradores", text="Borrador", text="Todos"')
        if draft_btn:
            print("\n-> Clickeando en filtro 'Borradores' / 'Todos'...")
            await draft_btn.click()
            await page.wait_for_timeout(2500)

        # Captura de pantalla para mostrarle al usuario la ubicación exacta
        shot_path = r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827\hotmart_pestana_borradores.png"
        await page.screenshot(path=shot_path)
        print(f"Captura guardada en: {shot_path}")

if __name__ == "__main__":
    asyncio.run(main())
