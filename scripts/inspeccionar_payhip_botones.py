import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if 'payhip.com' in pg.url][0]
        
        await payhip_page.goto('https://payhip.com/product/add/digital', wait_until='networkidle')

        js = """
        () => {
            return Array.from(document.querySelectorAll('button, input[type="submit"], a.btn, input[type="button"]')).map(e => ({
                id: e.id || '',
                name: e.name || '',
                class: e.className || '',
                text: e.innerText ? e.innerText.trim() : '',
                visible: e.offsetWidth > 0 && e.offsetHeight > 0
            }));
        }
        """
        btns = await payhip_page.evaluate(js)
        print("TODOS LOS BOTONES EN PAYHIP ADD DIGITAL:")
        for b in btns:
            print(" ", b)

if __name__ == "__main__":
    asyncio.run(main())
