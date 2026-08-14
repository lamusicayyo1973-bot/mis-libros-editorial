import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if 'payhip.com' in pg.url][0]
        await payhip_page.goto('https://payhip.com/products', wait_until='networkidle')
        await payhip_page.wait_for_timeout(2000)

        js = """
        () => {
            const items = Array.from(document.querySelectorAll('a[href*="/b/"], .product-title, td'));
            return items.map(e => ({
                text: e.innerText ? e.innerText.trim() : '',
                href: e.href || ''
            })).filter(x => x.text.length > 5);
        }
        """
        prods = await payhip_page.evaluate(js)
        print("===================================================")
        print("PRODUCTOS VISIBLES EN PAYHIP:")
        seen = set()
        for pr in prods:
            t = pr['text'].replace('\n', ' ')
            if t not in seen:
                seen.add(t)
                print("  •", t)
        print("===================================================")

if __name__ == "__main__":
    asyncio.run(main())
