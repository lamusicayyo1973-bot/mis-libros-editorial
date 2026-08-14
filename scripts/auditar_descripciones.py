# -*- coding: utf-8 -*-
import sys
import json
import requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")
TN_TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
TN_STORE = "8063094"
G_TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"

tn_headers = {"Authentication": f"bearer {TN_TOKEN}", "User-Agent": "LokiApp"}

# 1. Fetch Tiendanube products
tn_res = requests.get(f"https://api.tiendanube.com/v1/{TN_STORE}/products", headers=tn_headers, params={"per_page": 50}).json()
tn_map = {}
for p in tn_res:
    handle = p.get('handle', {}).get('es', '') if isinstance(p.get('handle'), dict) else p.get('handle')
    desc = p.get('description', {}).get('es', '') if isinstance(p.get('description'), dict) else p.get('description')
    tn_map[handle] = desc

# 2. Fetch Gumroad products
g_res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": G_TOKEN}).json().get('products', [])

print("======================================================================")
print("  AUDITORÍA DE DESCRIPCIONES (LOCAL vs TIENDANUBE vs GUMROAD)")
print("======================================================================\n")

for folder in sorted(BOOKS_DIR.glob("*")):
    if not folder.is_dir():
        continue
    ficha_path = folder / "ficha_producto.json"
    if not ficha_path.exists():
        print(f"[!] {folder.name}: Sin ficha_producto.json")
        continue

    with open(ficha_path, encoding='utf-8') as f:
        ficha = json.load(f)

    local_desc = ficha.get('descripcion', '')
    title = ficha.get('titulo', folder.name)

    print(f"📖 [{folder.name}]")
    print(f"   Título local: {title[:65]}")
    print(f"   Desc local ({len(local_desc)} chars): {local_desc[:80]}...")

    # Match in Tiendanube
    tn_match = None
    for h, d in tn_map.items():
        if folder.name in h or h in folder.name or folder.name.replace('-volumen-', '-la-estirpe-de-la-sangre-volumen-') in h:
            tn_match = d
            break

    if tn_match:
        has_desc = len(tn_match.strip()) > 0
        print(f"   -> Tiendanube: {'✅ Tiene descripción (' + str(len(tn_match)) + ' chars)' if has_desc else '❌ VACÍA'}")
    else:
        print("   -> Tiendanube: ❓ No mapeado directamente por handle")

    print()
