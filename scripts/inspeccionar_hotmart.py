import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        hotmart_pages = [pg for pg in context.pages if 'hotmart.com' in pg.url]
        if not hotmart_pages:
            print("No se encontró pestaña de Hotmart abierta.")
            return

        page = hotmart_pages[0]
        print("URL actual de Hotmart:", page.url)
        print("Título página:", await page.title())

        # Inspect links/buttons for creating product
        js = """
        () => {
            return Array.from(document.querySelectorAll('a, button')).map(e => ({
                tag: e.tagName,
                href: e.href || '',
                text: e.innerText ? e.innerText.trim().substring(0, 50) : '',
                class: e.className || ''
            })).filter(x => x.text.length > 0 && (
                x.text.toLowerCase().includes('producto') ||
                x.text.toLowerCase().includes('crear') ||
                x.text.toLowerCase().includes('nuevo') ||
                x.text.toLowerCase().includes('ebook') ||
                x.href.toLowerCase().includes('product')
            ));
        }
        """
        matches = await page.evaluate(js)
        print(f"Botones/links de creación encontrados ({len(matches)}):")
        for m in matches[:15]:
            print(" ", m)

if __name__ == "__main__":
    asyncio.run(main())
