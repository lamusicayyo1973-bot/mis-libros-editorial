import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if 'hotmart' in pg.url][0]
        
        await hotmart_page.goto('https://app.hotmart.com/products', wait_until='networkidle')
        await hotmart_page.wait_for_timeout(3000)

        js = """
        () => {
            const anchors = Array.from(document.querySelectorAll('a'));
            return anchors.map(a => ({
                text: a.innerText ? a.innerText.trim() : '',
                href: a.href || ''
            })).filter(x => x.href.includes('hotmart.com'));
        }
        """
        links = await hotmart_page.evaluate(js)
        print("LINKS EN HOTMART PRODUCTS:")
        seen = set()
        for l in links:
            t = l['text'].replace('\n', ' ')
            u = l['href']
            if u not in seen:
                seen.add(u)
                print("  •", t, "->", u)

if __name__ == "__main__":
    asyncio.run(main())
