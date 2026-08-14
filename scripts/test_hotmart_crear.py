import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        hotmart_page = [pg for pg in context.pages if 'hotmart.com' in pg.url][0]
        
        print("Haciendo clic en 'Crear producto' en Hotmart...")
        btn = await hotmart_page.query_selector("button:has-text('Crear producto')")
        if btn:
            await btn.click()
            await hotmart_page.wait_for_timeout(3000)

        print("URL actual de Hotmart:", hotmart_page.url)
        print("Título página:", await hotmart_page.title())

        # Inspect inputs on current Hotmart screen
        js = """
        () => {
            return Array.from(document.querySelectorAll('input, textarea, button, a')).map(e => ({
                tag: e.tagName,
                id: e.id || '',
                name: e.name || '',
                type: e.type || '',
                placeholder: e.placeholder || '',
                text: e.innerText ? e.innerText.trim().substring(0, 40) : ''
            })).filter(x => x.text.length > 0 or x.placeholder.length > 0 or x.name.length > 0);
        }
        """
        # (avoid 'or' syntax error in js)
        js_clean = """
        () => {
            return Array.from(document.querySelectorAll('input, textarea, button, a')).map(e => ({
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
        print(f"Elementos encontrados en formulario Hotmart ({len(elems)}):")
        for el in elems[:20]:
            if el['text'] or el['placeholder'] or el['name']:
                print(" ", el)

if __name__ == "__main__":
    asyncio.run(main())
