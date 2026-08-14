import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if 'payhip.com' in pg.url][0]
        
        js = """
        () => {
            const inputs = Array.from(document.querySelectorAll('input, textarea, .tiptap, .ql-editor, button[type="submit"]'));
            return inputs.map(e => ({
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                class: e.className || '',
                placeholder: e.placeholder || '',
                outer: e.outerHTML.substring(0, 150)
            }));
        }
        """
        res = await payhip_page.evaluate(js)
        print("Campos principales del formulario Payhip:")
        for r in res[:25]:
            print(" ", r)

if __name__ == "__main__":
    asyncio.run(main())
