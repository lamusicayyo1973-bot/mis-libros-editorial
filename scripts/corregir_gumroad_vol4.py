# -*- coding: utf-8 -*-
"""
Corrige el producto de Gumroad que esta como Volumen 10
y deberia ser Volumen 4.
ID Gumroad: Gi8a1mb1fWcRhsOM2wVGQA==
"""
import sys
import time
import base64
import json
import requests
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"
G_ID = "Gi8a1mb1fWcRhsOM2wVGQA=="
BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")
FOLDER = "oni-no-ketsuryu-volumen-4"

print("=" * 60)
print("  CORRIGIENDO GUMROAD: Vol10 -> Vol4")
print("=" * 60)

# Leer ficha
ficha_path = BOOKS_DIR / FOLDER / "ficha_producto.json"
with open(ficha_path, encoding="utf-8") as f:
    ficha = json.load(f)

titulo   = ficha["titulo"]
desc     = ficha["descripcion"]
precio   = ficha["precio"]
portada  = BOOKS_DIR / FOLDER / "portada.jpg"

print(f"\nTitulo nuevo: {titulo}")
print(f"Portada: {portada}")

# 1. Actualizar nombre y descripcion del producto
r = requests.put(
    f"https://api.gumroad.com/v2/products/{G_ID}",
    data={
        "access_token": TOKEN,
        "name": titulo,
        "description": desc,
        "price": int(precio * 100),  # en centavos
    }
)
if r.status_code == 200:
    print(f"\n[OK] Nombre y descripcion actualizados")
else:
    print(f"\n[X] Error al actualizar: {r.status_code} - {r.text[:120]}")

time.sleep(0.5)

# 2. Obtener portadas actuales y borrarlas
prod = requests.get(
    "https://api.gumroad.com/v2/products",
    params={"access_token": TOKEN}
).json()

covers = []
for p in prod.get("products", []):
    if p.get("id") == G_ID:
        covers = p.get("covers", [])
        break

print(f"\nPortadas actuales: {len(covers)}")
for c in covers:
    rd = requests.delete(
        f"https://api.gumroad.com/v2/products/{G_ID}/covers/{c['id']}",
        data={"access_token": TOKEN}
    )
    print(f"  -> Borrada portada {c['id']} -> {rd.status_code}")
    time.sleep(0.3)

# 3. Subir nueva portada desde Tiendanube (usando URL publica de Tiendanube Vol4)
# Primero conseguir la URL de Tiendanube para volumen 4
TN_TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
TN_STORE = "8063094"
TN_PID_VOL4 = 360187108  # ID Tiendanube de Oni Vol 4

tn_headers = {
    "Authentication": f"bearer {TN_TOKEN}",
    "User-Agent": "LokiApp"
}
tn_prod = requests.get(
    f"https://api.tiendanube.com/v1/{TN_STORE}/products/{TN_PID_VOL4}",
    headers=tn_headers
).json()

tn_imgs = tn_prod.get("images", [])
if tn_imgs:
    img_url = tn_imgs[0].get("src", "")
    print(f"\nURL de portada Tiendanube Vol4: {img_url[:80]}")

    # Subir a Gumroad usando la URL publica
    r2 = requests.post(
        f"https://api.gumroad.com/v2/products/{G_ID}/covers",
        data={"access_token": TOKEN, "url": img_url}
    )
    if r2.status_code == 200:
        print("[OK] Portada Vol4 asignada en Gumroad")
    else:
        print(f"[X] Error portada: {r2.status_code} - {r2.text[:120]}")
else:
    print("[!] No hay imagen en Tiendanube Vol4 para usar como URL")

print("\n" + "=" * 60)
print("  LISTO")
print("=" * 60)
