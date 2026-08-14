import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
STORE = "8063094"
headers = {
    "Authentication": f"bearer {TOKEN}",
    "User-Agent": "LokiApp"
}

# Obtener todos los productos (paginado)
all_products = []
page = 1
while True:
    r = requests.get(
        f"https://api.tiendanube.com/v1/{STORE}/products",
        headers=headers,
        params={"page": page, "per_page": 50}
    )
    batch = r.json()
    if not batch:
        break
    all_products.extend(batch)
    if len(batch) < 50:
        break
    page += 1

print(f"Total productos: {len(all_products)}\n")
for i, p in enumerate(all_products, 1):
    name_raw = p.get('name', {})
    name = name_raw.get('es', '') if isinstance(name_raw, dict) else name_raw
    handle_raw = p.get('handle', {})
    handle = handle_raw.get('es', '') if isinstance(handle_raw, dict) else handle_raw
    published = p.get('published', True)
    imgs = len(p.get('images', []))
    print(f"{i:02d}. [{p['id']}] {name[:55]}")
    print(f"     handle: {handle[:55]}")
    print(f"     publicado: {published} | imagenes: {imgs}")
    print()
