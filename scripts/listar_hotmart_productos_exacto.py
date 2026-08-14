# -*- coding: utf-8 -*-
import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACTS_DIR = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827")

async def listar_hotmart_productos():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        await hotmart_page.goto("https://app.hotmart.com/products", wait_until="networkidle")
        await hotmart_page.wait_for_timeout(3000)

        # Tomar captura visible
        screenshot_path = ARTIFACTS_DIR / "hotmart_productos_lista.png"
        try:
            await hotmart_page.screenshot(path=str(screenshot_path))
            print(f"[OK] Captura guardada en: {screenshot_path}")
        except Exception as e:
            print(f"[!] Captura omitida: {e}")

        # Extraer títulos de los productos en la vista de Hotmart
        js = """
        () => {
            const list = [];
            document.querySelectorAll('*').forEach(el => {
                const text = el.innerText ? el.innerText.trim() : '';
                if (text.length > 5 && text.length < 120) {
                    if (text.includes('Oni no Ketsuryū') || text.includes('KURO NO KINEKI') || text.includes('DE CERO A NEGOCIO') || text.includes('EL ALGORITMO')) {
                        list.push(text.replace(/\\n+/g, ' '));
                    }
                }
            });
            return Array.from(new Set(list));
        }
        """
        titulos = await hotmart_page.evaluate(js)

        print("\n======================================================================")
        print(f"   LISTADO DE LIBROS ENCONTRADOS EN HOTMART ({len(titulos)}):")
        print("======================================================================")
        for idx, t in enumerate(titulos, 1):
            print(f"  {idx:02d}. {t}")
        print("======================================================================")

if __name__ == "__main__":
    asyncio.run(listar_hotmart_productos())
