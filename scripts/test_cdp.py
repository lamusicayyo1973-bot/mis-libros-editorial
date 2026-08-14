import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("[OK] Conectado exitosamente a Chrome en puerto 9222!")
            print(f"Pestañas abiertas: {len(browser.contexts[0].pages)}")
            for idx, page in enumerate(browser.contexts[0].pages, 1):
                print(f"  {idx}. {page.title()} -> {page.url}")
        except Exception as e:
            print("[X] No se pudo conectar a Chrome en el puerto 9222.")
            print("    Detalle:", e)

if __name__ == "__main__":
    asyncio.run(main())
