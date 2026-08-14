# -*- coding: utf-8 -*-
"""
Sube portada.jpg exacta para Oni Vol 5-10 en Tiendanube.
Borra TODAS las imágenes del producto antes de subir.
"""
import sys
import time
import base64
import requests

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
STORE = "8063094"
BOOKS_DIR = r"C:\Proyectos\mis-libros-editorial\libros"

headers = {
    "Authentication": f"bearer {TOKEN}",
    "User-Agent": "LokiApp",
    "Content-Type": "application/json"
}

# Mapa explícito: ID de producto Tiendanube -> carpeta local
# Solo los 6 que están mal
TARGETS = {
    360187127: "oni-no-ketsuryu-volumen-5",
    360187141: "oni-no-ketsuryu-volumen-6",
    360187160: "oni-no-ketsuryu-volumen-7",
    360187172: "oni-no-ketsuryu-volumen-8",
    360187183: "oni-no-ketsuryu-volumen-9",
    360186970: "oni-no-ketsuryu-volumen-10",
}

print("=" * 60)
print("  CORRIGIENDO PORTADAS ONI VOL 5-10 EN TIENDANUBE")
print("=" * 60)

for pid, folder in TARGETS.items():
    import pathlib
    portada = pathlib.Path(BOOKS_DIR) / folder / "portada.jpg"
    print(f"\n[{folder}]")

    # 1. Obtener imágenes actuales del producto
    r = requests.get(
        f"https://api.tiendanube.com/v1/{STORE}/products/{pid}",
        headers=headers
    )
    prod = r.json()
    imgs = prod.get("images", [])
    print(f"  -> Imagenes actuales: {len(imgs)}")

    # 2. Borrar todas
    for img in imgs:
        rd = requests.delete(
            f"https://api.tiendanube.com/v1/{STORE}/products/{pid}/images/{img['id']}",
            headers=headers
        )
        print(f"  -> Borrada imagen {img['id']} -> {rd.status_code}")
        time.sleep(0.3)

    # 3. Subir portada.jpg correcta
    with open(portada, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    ru = requests.post(
        f"https://api.tiendanube.com/v1/{STORE}/products/{pid}/images",
        headers=headers,
        json={"filename": "portada.jpg", "attachment": b64}
    )
    if ru.status_code in [200, 201]:
        src = ru.json().get("src", "?")
        print(f"  [OK] Nueva portada subida: {src[:70]}")
    else:
        print(f"  [X] Error {ru.status_code}: {ru.text[:100]}")

    time.sleep(0.5)

print("\n" + "=" * 60)
print("  LISTO - Portadas Vol 5-10 corregidas")
print("=" * 60)
