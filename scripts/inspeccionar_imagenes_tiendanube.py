import sys
import os
import requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
STORE = "8063094"
BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

headers = {
    "Authentication": f"bearer {TOKEN}",
    "User-Agent": "LokiApp"
}

# Fetch all products from Tiendanube
r = requests.get(f"https://api.tiendanube.com/v1/{STORE}/products", headers=headers, params={"per_page": 50})
products = r.json()

print(f"Total productos en Tiendanube: {len(products)}")

out_dir = Path(r"C:\Proyectos\mis-libros-editorial\scratch_tiendanube_imgs")
out_dir.mkdir(exist_ok=True)

for i, p in enumerate(products, 1):
    pid = p.get('id')
    name = p.get('name', {}).get('es', '') if isinstance(p.get('name'), dict) else p.get('name')
    handle = p.get('handle', {}).get('es', '') if isinstance(p.get('handle'), dict) else p.get('handle')
    imgs = p.get('images', [])
    
    print(f"\n[{i:02d}] ID={pid} | Handle={handle}")
    print(f"     Nombre: {name}")
    if imgs:
        for idx_img, img in enumerate(imgs):
            src = img.get('src')
            print(f"     Img {idx_img+1}: {src}")
            # Download image to inspect
            filename = f"tn_{pid}_{idx_img+1}.jpg"
            img_data = requests.get(src).content
            filepath = out_dir / filename
            with open(filepath, "wb") as f:
                f.write(img_data)
            print(f"     Guardada localmente: {filepath} ({len(img_data)} bytes)")
    else:
        print("     [!] SIN IMAGENES")
