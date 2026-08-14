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
            return Array.from(document.querySelectorAll('a')).map(e => ({
                text: e.innerText ? e.innerText.trim() : '',
                href: e.href || ''
            })).filter(x => x.href.includes('/b/') or x.href.includes('/product/'));
        }
        """
        js_clean = """
        () => {
            return Array.from(document.querySelectorAll('a')).map(e => ({
                text: e.innerText ? e.innerText.trim() : '',
                href: e.href || ''
            })).filter(x => x.href.includes('/b/') || x.href.includes('/product/'));
        }
        """
        prods = await payhip_page.evaluate(js_clean)
        print("LISTA DE PRODUCTOS PUBLICADOS EN PAYHIP:")
        for pr in prods:
            print("  •", pr['text'], "->", pr['href'])

if __name__ == "__main__":
    asyncio.run(main())
