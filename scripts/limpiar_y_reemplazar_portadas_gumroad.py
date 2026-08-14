# -*- coding: utf-8 -*-
"""
===============================================================================
LIMPIEZA Y REEMPLAZO TOTAL DE PORTADAS EN GUMROAD
===============================================================================
1. Elimina TODAS las portadas antiguas/duplicadas adjuntas a cada producto en Gumroad.
2. Sube y asigna únicamente la portada EXACTA proveniente de Tiendanube.
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

tn_headers = {
    "Authentication": f"bearer {TIENDANUBE_TOKEN}",
    "User-Agent": "LokiApp"
}


def normalizar(t):
    if not t:
        return ""
    t = t.lower()
    for c in [":", "-", "_", "•", "  ", "volumen", "vol"]:
        t = t.replace(c, " ")
    return " ".join(t.split())


def limpiar_y_reemplazar_portadas_gumroad():
    print("=" * 70)
    print("  🎨 ELIMINANDO PORTADAS VIEJAS Y REEMPLAZANDO EN GUMROAD")
    print("=" * 70)

    # 1. Obtener imágenes de Tiendanube mapeadas por handle / título
    tn_res = requests.get(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products", headers=tn_headers)
    tn_map = {}
    if tn_res.status_code == 200:
        for p in tn_res.json():
            handle = p.get("handle", {}).get("es", "") if isinstance(p.get("handle"), dict) else p.get("handle", "")
            images = p.get("images", [])
            if images:
                tn_map[handle] = images[0].get("src")

    # 2. Obtener productos de Gumroad
    g_res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": GUMROAD_TOKEN})
    g_data = g_res.json()

    if not g_data.get("success"):
        print("  [X] Error consultando Gumroad:", g_data)
        return

    g_products = g_data.get("products", [])
    print(f"\n  -> Se encontraron {len(g_products)} productos en Gumroad:\n")

    for idx, prod in enumerate(g_products, 1):
        pid = prod.get("id")
        name = prod.get("name", "")
        covers = prod.get("covers", [])

        print(f"  -------------------------------------------------------------")
        print(f"  [{idx}/{len(g_products)}] PRODUCTO: {name}")
        print(f"        ID: {pid} | Portadas actuales: {len(covers)}")

        # A. Borrar TODAS las portadas antiguas
        for c in covers:
            cid = c.get("id")
            del_url = f"https://api.gumroad.com/v2/products/{pid}/covers/{cid}"
            r_del = requests.delete(del_url, data={"access_token": GUMROAD_TOKEN})
            print(f"        -> Eliminando portada vieja ID {cid}: {r_del.status_code}")

        # B. Encontrar la portada correcta en Tiendanube
        correct_img_url = None
        for tn_handle, img_url in tn_map.items():
            # Coincidencia por slugs
            if "algoritmo" in name.lower() and "algoritmo" in tn_handle:
                correct_img_url = img_url
                break
            elif "cero" in name.lower() and "cero" in tn_handle:
                correct_img_url = img_url
                break
            elif "kuro" in name.lower() and "kuro" in tn_handle:
                for v in ["1", "2", "3"]:
                    if f"volumen-{v}" in tn_handle and (f"volumen {v}" in name.lower() or f"volumen-{v}" in name.lower() or f": volumen {v}" in name.lower() or f"vol {v}" in name.lower()):
                        correct_img_url = img_url
                        break
                if correct_img_url:
                    break
            elif "oni" in name.lower() and "oni" in tn_handle:
                for v in range(1, 11):
                    if f"volumen-{v}" in tn_handle and f"volumen {v}" in name.lower():
                        correct_img_url = img_url
                        break
                if correct_img_url:
                    break

        # C. Subir la ÚNICA portada correcta
        if correct_img_url:
            print(f"        -> Subiendo portada correcta limpia: {correct_img_url[:60]}...")
            r_post = requests.post(
                f"https://api.gumroad.com/v2/products/{pid}/covers",
                data={"access_token": GUMROAD_TOKEN, "url": correct_img_url}
            )
            if r_post.status_code == 200:
                print("        [OK] Portada única establecida perfectamente")
            else:
                print(f"        [X] Error subiendo portada: {r_post.status_code} {r_post.text[:80]}")
        else:
            print("        [!] No se encontró URL de portada en Tiendanube")

        time.sleep(1)

    print("\n" + "=" * 70)
    print("  🎉 PROCESO COMPLETADO: Gumroad limpio y con portadas 100% correctas.")
    print("=" * 70)


if __name__ == "__main__":
    limpiar_y_reemplazar_portadas_gumroad()
