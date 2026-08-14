import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        # Extraer todos los labels, selects, inputs y textos de error
        js = """
        () => {
            const inputs = Array.from(document.querySelectorAll('input, select, textarea, label, [class*="error"], [class*="invalid"]')).map(e => ({
                tag: e.tagName,
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                class: e.className || '',
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : ''
            }));
            return inputs.filter(x => x.text.length > 0 || x.id.length > 0 || x.name.length > 0);
        }
        """
        data = await hotmart_page.evaluate(js)
        print("ESTRUCTURA DE CAMPOS EN HOTMART ADD 4 INFO:")
        for item in data[:50]:
            print("  •", item)

if __name__ == "__main__":
    asyncio.run(main())
