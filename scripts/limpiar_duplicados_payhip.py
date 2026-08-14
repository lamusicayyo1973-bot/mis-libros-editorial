# -*- coding: utf-8 -*-
"""
===============================================================================
LIMPIADOR DE DUPLICADOS EN PAYHIP VÍA CDP (PUERTO 9222)
===============================================================================
Obtiene la lista completa de productos en Payhip, detecta títulos duplicados,
y elimina los duplicados para dejar únicamente 1 copia de cada libro.
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

async def limpiar_payhip_duplicados():
    print("=" * 70)
    print("  LIMPIANDO DUPLICADOS EN PAYHIP VÍA CDP")
    print("=" * 70)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("[X] No se pudo conectar a Brave en el puerto 9222:", e)
            return

        context = browser.contexts[0]
        payhip_pages = [pg for pg in context.pages if "payhip.com" in pg.url]
        page = payhip_pages[0] if payhip_pages else await context.new_page()

        await page.goto("https://payhip.com/products", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Extraer filas de productos con sus títulos y links de edición/borrado
        js = """
        () => {
            const rows = Array.from(document.querySelectorAll('tr, .product-item, .js-product-row'));
            const result = [];
            rows.forEach(r => {
                const titleLink = r.querySelector('a[href*="/b/"], .product-title, a.js-product-title');
                const editLink  = r.querySelector('a[href*="/product/edit/"]');
                const deleteBtn = r.querySelector('button.js-delete-product, a.js-delete-product, .js-delete-btn');
                if (titleLink && editLink) {
                    result.append ? result.append({
                        title: titleLink.innerText.trim(),
                        id: editLink.href.split('/product/edit/')[1] || '',
                        url: titleLink.href
                    }) : result.push({
                        title: titleLink.innerText.trim(),
                        id: editLink.href.split('/product/edit/')[1] || '',
                        url: titleLink.href
                    });
                }
            });
            return result;
        }
        """
        prods = await page.evaluate(js)
        print(f"\nTotal items encontrados en la lista de Payhip: {len(prods)}\n")

        vistos = {}
        duplicados = []

        for p_item in prods:
            t = p_item["title"]
            pid = p_item["id"]
            if t in vistos:
                duplicados.append(p_item)
            else:
                vistos[t] = p_item

        print(f"Únicos: {len(vistos)} | Duplicados a eliminar: {len(duplicados)}\n")

        for dup in duplicados:
            pid = dup["id"]
            title = dup["title"]
            print(f"🗑️ Eliminando duplicado: {title[:50]} (ID: {pid})...")
            # Navegar a la edición del producto duplicado o llamar a su delete
            await page.goto(f"https://payhip.com/product/edit/{pid}", wait_until="networkidle")
            await page.wait_for_timeout(1000)

            # Buscar botón de borrar o archivar
            delete_btn = await page.query_selector('a.js-delete-product, button:has-text("Delete"), button:has-text("Archive"), #btn-delete-product')
            if delete_btn:
                await delete_btn.click()
                await page.wait_for_timeout(1000)
                confirm = await page.query_selector('button.confirm, button:has-text("OK"), button:has-text("Yes")')
                if confirm:
                    await confirm.click()
                    await page.wait_for_timeout(2000)
                print(f"   [OK] Eliminado ID: {pid}")
            else:
                print(f"   [!] No se encontró botón de borrado directo para ID: {pid}")

        # Volver a la lista de productos
        await page.goto("https://payhip.com/products", wait_until="networkidle")
        print("\n" + "=" * 70)
        print("  LIMPIEZA DE DUPLICADOS EN PAYHIP FINALIZADA")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(limpiar_payhip_duplicados())
