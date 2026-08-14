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
            const rows = Array.from(document.querySelectorAll('tr'));
            return rows.map(r => {
                const a = r.querySelector('a[href*="/b/"]');
                const ed = r.querySelector('a[href*="/product/edit/"]');
                return {
                    title: a ? a.innerText.trim() : '',
                    url: a ? a.href : '',
                    edit_url: ed ? ed.href : ''
                };
            }).filter(x => x.title.length > 0);
        }
        """
        prods = await payhip_page.evaluate(js)
        print(f"TOTAL PRODUCTOS EN PAYHIP: {len(prods)}\n")
        for i, pr in enumerate(prods, 1):
            print(f"{i:02d}. {pr['title']}")
            print(f"     URL pública: {pr['url']}")
            print(f"     URL edición: {pr['edit_url']}\n")

if __name__ == "__main__":
    asyncio.run(main())
