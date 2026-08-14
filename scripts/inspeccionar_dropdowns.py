import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        js = """
        () => {
            const divs = Array.from(document.querySelectorAll('div, button, span')).map(e => ({
                tag: e.tagName,
                class: e.className || '',
                id: e.id || '',
                placeholder: e.getAttribute('placeholder') || '',
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : ''
            }));
            return divs.filter(x => x.text.includes('Seleccionar') || x.text.includes('Categoría') || x.text.includes('Idioma') || x.text.includes('país') || x.class.includes('select'));
        }
        """
        data = await hotmart_page.evaluate(js)
        print("DROPDOWNS EN HOTMART INFO:")
        for item in data[:30]:
            print("  •", item)

if __name__ == "__main__":
    asyncio.run(main())
