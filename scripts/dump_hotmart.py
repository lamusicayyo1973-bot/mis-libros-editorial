import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        await hotmart_page.goto("https://app.hotmart.com/products", wait_until="networkidle")
        await hotmart_page.wait_for_timeout(3000)

        # Imprimir todo el innerText de la página para ver las secciones
        body_text = await hotmart_page.evaluate("() => document.body.innerText")
        print("--- TEXTO DE LA PAGINA DE HOTMART PRODUCTS ---")
        lines = [line.strip() for line in body_text.split("\n") if line.strip()]
        for line in lines[:60]:
            print("  ", line)

if __name__ == "__main__":
    asyncio.run(main())
