import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if 'payhip.com' in pg.url][0]
        
        js = """
        () => {
            const elems = Array.from(document.querySelectorAll('input, textarea, select, label, button, .ql-editor, div[contenteditable="true"]'));
            return elems.map(e => ({
                tag: e.tagName,
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                class: e.className || '',
                placeholder: e.placeholder || '',
                text: e.innerText ? e.innerText.trim().substring(0, 40) : ''
            }));
        }
        """
        info = await payhip_page.evaluate(js)
        print(f"Total elementos encontrados: {len(info)}")
        for item in info:
            print(item)

if __name__ == "__main__":
    asyncio.run(main())
