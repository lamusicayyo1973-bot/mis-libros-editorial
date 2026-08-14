import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "hotmart" in pg.url][0]
        print("URL actual en Brave:", page.url)

        js = """
        () => {
            const tabs = Array.from(document.querySelectorAll('a, button, span, div, h1, h2, h3')).map(e => ({
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : ''
            }));
            return tabs.filter(x => x.text.length > 2 && x.text.length < 50);
        }
        """
        elements = await page.evaluate(js)
        print("\nELEMENTOS VISIBLES EN PANTALLA:")
        for el in elements[:30]:
            print(f"  • {el['text']}")

if __name__ == "__main__":
    asyncio.run(main())
