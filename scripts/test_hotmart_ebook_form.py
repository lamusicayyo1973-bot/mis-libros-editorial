import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if 'hotmart.com' in pg.url][0]
        
        print("Haciendo clic en 'Registrar Ebook' en Hotmart...")
        btn = await hotmart_page.query_selector('button[id="4"]')
        if not btn:
            btn = await hotmart_page.query_selector("text=Registrar Ebook")
        if not btn:
            btn = await hotmart_page.query_selector("text=eBook")

        if btn:
            await btn.click()
            await hotmart_page.wait_for_timeout(3000)

        print("URL actual de Hotmart:", hotmart_page.url)
        print("Título página:", await hotmart_page.title())

        js_clean = """
        () => {
            return Array.from(document.querySelectorAll('input, textarea, select, button, div[contenteditable="true"], .ql-editor')).map(e => ({
                tag: e.tagName,
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                placeholder: e.placeholder || '',
                text: e.innerText ? e.innerText.trim().substring(0, 40) : ''
            }));
        }
        """
        elems = await hotmart_page.evaluate(js_clean)
        print(f"Campos del formulario Ebook ({len(elems)}):")
        for el in elems:
            if el['placeholder'] or el['name'] or el['id'] or 'file' in el['type']:
                print(" ", el)

if __name__ == "__main__":
    asyncio.run(main())
