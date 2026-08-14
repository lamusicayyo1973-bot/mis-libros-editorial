import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        payhip_page = [pg for pg in context.pages if 'payhip.com' in pg.url][0]
        
        print('Navegando a https://payhip.com/product/add/digital...')
        await payhip_page.goto('https://payhip.com/product/add/digital', wait_until='networkidle')
        await payhip_page.wait_for_timeout(2000)

        print('URL:', payhip_page.url)
        print('Título:', await payhip_page.title())

        # Inspect all inputs and textareas
        js = """
        () => {
            return Array.from(document.querySelectorAll('input, textarea, div[contenteditable="true"], .ql-editor, button, a.btn')).map(e => ({
                tag: e.tagName,
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                class: e.className || '',
                placeholder: e.placeholder || '',
                text: e.innerText ? e.innerText.trim().substring(0, 30) : ''
            }));
        }
        """
        elems = await payhip_page.evaluate(js)
        print(f'Total elementos en formulario ({len(elems)}):')
        for el in elems:
            print(' ', el)

if __name__ == "__main__":
    asyncio.run(main())
