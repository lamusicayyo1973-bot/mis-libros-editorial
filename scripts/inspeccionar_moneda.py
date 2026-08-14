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
            const list = Array.from(document.querySelectorAll('div, span, button, select, option')).map(e => ({
                tag: e.tagName,
                class: e.className || '',
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : ''
            }));
            return list.filter(x => x.text.includes('Dólar') || x.text.includes('USD') || x.text.includes('Moneda') || x.text.includes('Euro'));
        }
        """
        data = await hotmart_page.evaluate(js)
        print("ELEMENTOS DE MONEDA EN PRICING:")
        for item in data[:20]:
            print("  •", item)

if __name__ == "__main__":
    asyncio.run(main())
