# -*- coding: utf-8 -*-
"""
===============================================================================
CORRECTOR DE TÍTULOS EN PAYHIP
===============================================================================
Actualiza los títulos de Kuro no Kineki en Payhip para incluir explícitamente
el número de Volumen y Subtítulo.
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

TITULOS_CORRECTOS = {
    "JgoYS": "KURO NO KINEKI (Ecos de Tinta Negra) - Volumen 1: El Precio del Primer Paso",
    "YpJPq": "KURO NO KINEKI (Ecos de Tinta Negra) - Volumen 2: El Choque de los Tres Soles",
    "rIbUa": "KURO NO KINEKI (Ecos de Tinta Negra) - Volumen 3: El Despertar de los Creadores",
}

async def arreglar_titulos():
    print("======================================================================")
    print("  ACTUALIZANDO TÍTULOS DE KURO NO KINEKI EN PAYHIP")
    print("======================================================================")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if "payhip.com" in pg.url][0]

        for pid, titulo in TITULOS_CORRECTOS.items():
            print(f"\n[ID: {pid}] Actualizando a: {titulo}")
            await payhip_page.goto(f"https://payhip.com/product/edit/{pid}", wait_until="networkidle")
            await payhip_page.wait_for_timeout(1500)

            title_el = await payhip_page.query_selector('#p_name, input[name="p_name"]')
            if title_el:
                await title_el.fill(titulo)
                print("   -> Título editado")

            submit_btn = await payhip_page.query_selector('#addsubmit')
            if submit_btn:
                await submit_btn.click()
                await payhip_page.wait_for_timeout(3000)
                print(f"   [OK] Guardado ID {pid}")

        await payhip_page.goto("https://payhip.com/products", wait_until="networkidle")
        print("\n" + "=" * 70)
        print("  TÍTULOS ACTUALIZADOS EN PAYHIP")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(arreglar_titulos())
