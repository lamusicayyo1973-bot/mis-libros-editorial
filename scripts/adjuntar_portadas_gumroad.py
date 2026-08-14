# -*- coding: utf-8 -*-
"""
===============================================================================
ADJUNTAR PORTADAS DE PRODUCTO EN GUMROAD VÍA API
===============================================================================
Obtiene las portadas de los productos desde Tiendanube / Local y las adjunta
como portada principal (main_cover) a los productos de Gumroad.
===============================================================================
"""

import sys
import json
import time
import requests
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

GUMROAD_TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"
TIENDANUBE_TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
TIENDANUBE_STORE_ID = "8063094"

BASE_DIR = Path(r"C:\Proyectos\mis-libros-editorial")
BOOKS_DIR = BASE_DIR / "libros"


def normalizar_texto(txt):
    if not txt:
        return ""
    txt = txt.lower()
    for c in [":", "-", "_", "•", "  ", "volumen", "vol"]:
        txt = txt.replace(c, " ")
    return " ".join(txt.split())


def adjuntar_portadas_gumroad():
    print("=" * 70)
    print("  🎨 ADJUNTANDO PORTADAS PRINCIPALES A PRODUCTOS DE GUMROAD")
    print("=" * 70)

    # 1. Obtener productos de Tiendanube con sus URLs de imagen
    tn_headers = {
        "Authentication": f"bearer {TIENDANUBE_TOKEN}",
        "User-Agent": "LokiApp"
    }
    print("\n  [1/3] Obteniendo imágenes de Tiendanube...")
    tn_res = requests.get(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products", headers=tn_headers)
    tn_map = {}
    if tn_res.status_code == 200:
        for p in tn_res.json():
            nombre = p.get("name", {}).get("es", "") if isinstance(p.get("name"), dict) else p.get("name", "")
            images = p.get("images", [])
            if images and len(images) > 0:
                img_url = images[0].get("src")
                if img_url:
                    tn_map[normalizar_texto(nombre)] = img_url

    print(f"        -> {len(tn_map)} imágenes públicas encontradas.")

    # 2. Obtener productos de Gumroad
    print("\n  [2/3] Obteniendo productos de Gumroad...")
    g_res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": GUMROAD_TOKEN})
    g_data = g_res.json()

    if not g_data.get("success"):
        print("  [X] Error al obtener productos de Gumroad:", g_data)
        return

    g_products = g_data.get("products", [])
    print(f"        -> {len(g_products)} productos en Gumroad.")

    # 3. Vincular portadas
    print("\n  [3/3] Asignando portadas en Gumroad...")
    for idx, prod in enumerate(g_products, 1):
        prod_id = prod.get("id")
        name = prod.get("name", "")
        norm_name = normalizar_texto(name)
        covers = prod.get("covers", [])

        if len(covers) > 0:
            print(f"  [{idx}/{len(g_products)}] {name[:45]}... -> YA TIENE PORTADA")
            continue

        # Buscar URL de la portada
        img_url = None
        for tn_title, url in tn_map.items():
            if norm_name in tn_title or tn_title in norm_name:
                img_url = url
                break

        if img_url:
            print(f"  [{idx}/{len(g_products)}] Subiendo portada para: {name[:45]}...")
            r = requests.post(
                f"https://api.gumroad.com/v2/products/{prod_id}/covers",
                data={"access_token": GUMROAD_TOKEN, "url": img_url}
            )
            res_json = r.json()
            if res_json.get("success"):
                print(f"        [✓] Portada asignada exitosamente")
            else:
                print(f"        [!] Aviso: {res_json}")
        else:
            print(f"  [{idx}/{len(g_products)}] ⚠️ No se encontró imagen pública para: {name[:45]}")

        time.sleep(1)

    print("\n" + "=" * 70)
    print("  🎉 PROCESO COMPLETADO: Portadas asignadas en Gumroad.")
    print("=" * 70)


if __name__ == "__main__":
    adjuntar_portadas_gumroad()
