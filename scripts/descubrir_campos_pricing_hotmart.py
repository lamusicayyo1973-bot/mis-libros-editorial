import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if "hotmart" in pg.url][0]

        await hotmart_page.goto("https://app.hotmart.com/products/add/4/pricing", wait_until="networkidle")
        await hotmart_page.wait_for_timeout(2000)

        js = """
        () => {
            const inputs = Array.from(document.querySelectorAll('input, select, textarea, button, label, .hot-form')).map(e => ({
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
        print("ESTRUCTURA DE CAMPOS EN PRICING HOTMART:")
        for d in data[:50]:
            if len(d['text']) > 0 or d['id'] or d['name']:
                print("  •", d)

if __name__ == "__main__":
    asyncio.run(main())
