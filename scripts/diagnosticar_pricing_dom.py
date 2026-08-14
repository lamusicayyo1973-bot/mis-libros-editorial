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
            const inputs = Array.from(document.querySelectorAll('input, select, textarea, button, label, .invalid-feedback, [class*="error"]')).map(e => ({
                tag: e.tagName,
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                class: e.className || '',
                text: e.innerText ? e.innerText.trim().replace(/\\n+/g, ' ') : ''
            }));
            return inputs;
        }
        """
        data = await hotmart_page.evaluate(js)
        print("DOM EN HOTMART PRICING:")
        for item in data:
            if len(item['text']) > 0 or item['id'] or item['name']:
                print("  •", item)

if __name__ == "__main__":
    asyncio.run(main())
