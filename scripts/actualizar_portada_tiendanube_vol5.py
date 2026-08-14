# -*- coding: utf-8 -*-
import sys, json, requests, base64
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Credenciales activas de Tiendanube
ACCESS_TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
STORE_ID = "8063094"
HEADERS = {
    "Authentication": f"bearer {ACCESS_TOKEN}",
    "User-Agent": "LokiApp",
    "Content-Type": "application/json"
}

VOL5_FOLDER = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5")
PORTADA_PATH = VOL5_FOLDER / "portada.jpg"

def actualizar_tiendanube():
    print("1. Buscando producto Volumen 5 en Tiendanube...")
    url_prods = f"https://api.tiendanube.com/v1/{STORE_ID}/products?per_page=200"
    resp = requests.get(url_prods, headers=HEADERS)
    if resp.status_code != 200:
        print("Error al consultar Tiendanube:", resp.text)
        return

    products = resp.json()
    vol5_product = None
    for p in products:
        name_raw = p.get('name', {})
        name = name_raw.get('es', '') if isinstance(name_raw, dict) else str(name_raw)
        if "Volumen 5" in name or "volumen-5" in str(p.get("handle", "")):
            vol5_product = p
            break

    if not vol5_product:
        print("No se encontró el producto Volumen 5 en Tiendanube.")
        return

    prod_id = vol5_product["id"]
    name_str = vol5_product['name']['es'] if isinstance(vol5_product['name'], dict) else vol5_product['name']
    print(f"Producto encontrado! ID: {prod_id} | Titulo: {name_str}")

    # 2. Borrar imagenes viejas
    images = vol5_product.get("images", [])
    for img in images:
        img_id = img["id"]
        del_url = f"https://api.tiendanube.com/v1/{STORE_ID}/products/{prod_id}/images/{img_id}"
        requests.delete(del_url, headers=HEADERS)
        print(f"   Imagen vieja eliminada: {img_id}")

    # 3. Subir nueva portada en base64
    with open(PORTADA_PATH, "rb") as f:
        encoded_img = base64.b64encode(f.read()).decode('utf-8')

    img_payload = {
        "attachment": encoded_img,
        "filename": "portada_volumen_5.jpg",
        "position": 1
    }

    add_url = f"https://api.tiendanube.com/v1/{STORE_ID}/products/{prod_id}/images"
    res_img = requests.post(add_url, headers=HEADERS, json=img_payload)
    if res_img.status_code in (200, 201):
        print("✅ [TIENDANUBE] Portada del Volumen 5 actualizada 100% con exito!")
    else:
        print("Error al subir nueva imagen a Tiendanube:", res_img.text)

if __name__ == "__main__":
    actualizar_tiendanube()
