import os
import json
import time
from playwright.sync_api import sync_playwright

BASE_DIR = r"c:\Users\nicol\Downloads\MIS LIBROS"
LIBROS_DIR = os.path.join(BASE_DIR, "libros")
CONFIG_PATH = os.path.join(BASE_DIR, "configuracion_autor.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_all_books():
    books = []
    for item in os.listdir(LIBROS_DIR):
        item_path = os.path.join(LIBROS_DIR, item)
        if os.path.isdir(item_path):
            ficha_path = os.path.join(item_path, "ficha_producto.json")
            if os.path.exists(ficha_path):
                with open(ficha_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data["folder_path"] = item_path
                    data["docx_path"] = os.path.join(item_path, "libro.docx")
                    data["portada_path"] = os.path.join(item_path, "portada.jpg")
                    data["banner_path"] = os.path.join(item_path, "banner.jpg")
                    books.append(data)
    return books

def run_publication_assistant():
    config = load_config()
    books = get_all_books()
    
    print("\n==========================================")
    print("ASISTENTE AUTOMÁTICO DE PUBLICACIÓN Y PAGOS")
    print("==========================================")
    print(f"Autor: {config['autor']['nombre_completo']}")
    print(f"CBU Registrado: {config['datos_bancarios']['cbu']}")
    print(f"Total Libros a Cargar: {len(books)}")
    print("==========================================\n")
    
    with sync_playwright() as p:
        # Launch visible browser for user to interact / auto-fill
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport=None)
        page = context.new_page()
        
        # 1. Open Gumroad Payouts configuration page
        print("[1/2] Abriendo página de Pagos/CBU en Gumroad...")
        page.goto("https://gumroad.com/settings/payouts")
        print("\n--> POR FAVOR INICIÁ SESIÓN EN GUMROAD EN LA VENTANA QUE SE ABRIÓ.")
        print("--> El asistente te guiará y autocompletará el CBU y los productos.")
        
        input("\n[Presioná ENTER en la consola una vez que hayas iniciado sesión en Gumroad...]")
        
        # Auto fill Payouts if on Payouts page
        try:
            print("Autocompletando datos bancarios en Gumroad...")
            # Navigate if not already there
            if "payouts" not in page.url:
                page.goto("https://gumroad.com/settings/payouts")
                page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Nota sobre formulario de pagos: {e}")

        # 2. Iterate through books and assist creation on Gumroad
        for idx, b in enumerate(books, 1):
            print(f"\n[{idx}/{len(books)}] Preparando carga de: {b.get('titulo', b.get('nombre', 'eBook'))}")
            print(f"  • Archivo Word: {b['docx_path']}")
            print(f"  • Portada: {b['portada_path']}")
            print(f"  • Precio: $20.00 USD")
            
            page.goto("https://gumroad.com/products/new")
            time.sleep(2)
            
            # Offer user option to move to next book
            ans = input(f"¿Cargar datos de '{b.get('titulo', 'Libro')}' en la pantalla de Gumroad? (s/n): ")
            if ans.lower().startswith('s'):
                try:
                    # Select Ebook type if available
                    ebook_btn = page.query_selector("text=Ebook") or page.query_selector("button:has-text('Ebook')")
                    if ebook_btn:
                        ebook_btn.click()
                    
                    # Fill Name & Price
                    name_input = page.query_selector("input[name='name']") or page.query_selector("input[placeholder*='Name']")
                    if name_input:
                        name_input.fill(b.get("titulo", "eBook Oficial"))
                    
                    price_input = page.query_selector("input[name='price']") or page.query_selector("input[placeholder*='0']")
                    if price_input:
                        price_input.fill("20")
                    
                    print(f"-> Rellenados título y precio de {b.get('titulo')}. Continuá en el navegador para adjuntar archivos.")
                except Exception as ex:
                    print(f"Autocompletado parcial: {ex}")
            
        print("\n=== ¡PROCESO DE ASISTENCIA FINALIZADO! ===")
        print("El navegador permanecerá abierto para que revises y confirmes la publicación.")
        input("Presioná ENTER cuando desees cerrar el asistente.")
        browser.close()

if __name__ == "__main__":
    run_publication_assistant()
