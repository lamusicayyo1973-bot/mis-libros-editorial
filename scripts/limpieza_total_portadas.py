# -*- coding: utf-8 -*-
"""
===============================================================================
LIMPIEZA TOTAL Y REEMPLAZO 100% LIMPIO DE PORTADAS (TIENDANUBE + GUMROAD)
===============================================================================
1. Tiendanube: Elimina TODAS las imágenes adjuntas a cada producto y sube
   únicamente el archivo portada.jpg exacto desde la carpeta local del libro.
2. Gumroad: Elimina TODAS las portadas antiguas adjuntas a cada producto y
   sube únicamente la portada recién instalada en Tiendanube.
===============================================================================
"""

import sys
import json
import time
import base64
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

tn_headers = {
    "Authentication": f"bearer {TIENDANUBE_TOKEN}",
    "User-Agent": "LokiApp",
    "Content-Type": "application/json"
}


def mapear_carpetas_locales():
    folders = {}
    for f in BOOKS_DIR.iterdir():
        if f.is_dir():
            slug = f.name
            portada = f / "portada.jpg"
            if portada.exists():
                folders[slug] = portada
    return folders


def limpiar_tiendanube(mapa_portadas):
    print("=" * 70)
    print("  [1/2] TIENDANUBE: BORRANDO IMÁGENES VIEJAS Y SUBIENDO PORTADA.JPG")
    print("=" * 70)

    res = requests.get(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products", headers=tn_headers)
    if res.status_code != 200:
        print("  [X] Error consultando Tiendanube:", res.status_code)
        return {}

    products = res.json()
    print(f"\n  -> Total productos en Tiendanube: {len(products)}\n")

    tn_final_images = {}

    for idx, p in enumerate(products, 1):
        pid = p.get("id")
        handle = p.get("handle", {}).get("es", "") if isinstance(p.get("handle"), dict) else p.get("handle", "")
        name = p.get("name", {}).get("es", "") if isinstance(p.get("name"), dict) else p.get("name", "")

        print(f"  -------------------------------------------------------------")
        print(f"  [{idx}/{len(products)}] {name} (handle: {handle})")

        # Encontrar la portada local exacta
        target_portada = None
        for slug, img_path in mapa_portadas.items():
            if slug in handle or handle in slug:
                target_portada = img_path
                break

        if not target_portada:
            print("        [!] No se pudo emparejar la carpeta local")
            continue

        # A. BORRAR TODAS LAS IMÁGENES ANTERIORES EN TIENDANUBE
        images = p.get("images", [])
        print(f"        -> Eliminando {len(images)} imágenes anteriores...")
        for img in images:
            img_id = img.get("id")
            requests.delete(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{pid}/images/{img_id}", headers=tn_headers)
            time.sleep(0.3)

        # B. SUBIR LA PORTADA.JPG EXACTA EN BASE64
        print(f"        -> Subiendo {target_portada.name} limpia en Base64...")
        with open(target_portada, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")

        payload = {"filename": "portada.jpg", "attachment": b64_data}
        r_post = requests.post(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{pid}/images", headers=tn_headers, json=payload)
        
        if r_post.status_code in [200, 201]:
            post_data = r_post.json()
            new_src = post_data.get("src")
            tn_final_images[handle] = new_src
            print("        [OK] Portada.jpg instalada como única imagen en Tiendanube")
        else:
            print(f"        [X] Error subiendo imagen: {r_post.status_code}")

        time.sleep(1)

    return tn_final_images


def limpiar_gumroad(tn_final_images):
    print("\n" + "=" * 70)
    print("  [2/2] GUMROAD: BORRANDO PORTADAS VIEJAS Y ASIGNANDO PORTADA LOKI")
    print("=" * 70)

    res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": GUMROAD_TOKEN})
    g_data = res.json()
    g_prods = g_data.get("products", [])

    print(f"\n  -> Total productos en Gumroad: {len(g_prods)}\n")

    for idx, gp in enumerate(g_prods, 1):
        g_id = gp.get("id")
        g_name = gp.get("name", "")
        covers = gp.get("covers", [])

        print(f"  -------------------------------------------------------------")
        print(f"  [{idx}/{len(g_prods)}] {g_name[:50]}")

        # A. BORRAR TODAS LAS PORTADAS VIEJAS EN GUMROAD
        print(f"        -> Eliminando {len(covers)} portadas antiguas en Gumroad...")
        for c in covers:
            cid = c.get("id")
            requests.delete(f"https://api.gumroad.com/v2/products/{g_id}/covers/{cid}", data={"access_token": GUMROAD_TOKEN})
            time.sleep(0.3)

        # B. BUSCAR URL DE PORTADA EN TIENDANUBE
        matching_url = None
        for tn_handle, img_url in tn_final_images.items():
            if "algoritmo" in g_name.lower() and "algoritmo" in tn_handle:
                matching_url = img_url
                break
            elif "cero" in g_name.lower() and "cero" in tn_handle:
                matching_url = img_url
                break
            elif "kuro" in g_name.lower() and "kuro" in tn_handle:
                for v in ["1", "2", "3"]:
                    if f"volumen-{v}" in tn_handle and (f"volumen {v}" in g_name.lower() or f"volumen-{v}" in g_name.lower() or f"vol {v}" in g_name.lower()):
                        matching_url = img_url
                        break
                if matching_url:
                    break
            elif "oni" in g_name.lower() and "oni" in tn_handle:
                for v in range(1, 11):
                    if f"volumen-{v}" in tn_handle and f"volumen {v}" in g_name.lower():
                        matching_url = img_url
                        break
                if matching_url:
                    break

        # C. ASIGNAR LA PORTADA ÚNICA EN GUMROAD
        if matching_url:
            print(f"        -> Subiendo portada única: {matching_url[:50]}...")
            r_cover = requests.post(f"https://api.gumroad.com/v2/products/{g_id}/covers", data={"access_token": GUMROAD_TOKEN, "url": matching_url})
            if r_cover.status_code == 200:
                print("        [OK] Portada única establecida perfectamente en Gumroad")
            else:
                print(f"        [X] Error subiendo portada a Gumroad: {r_cover.status_code}")
        else:
            print("        [!] No se encontró imagen correspondiente de Tiendanube")

        time.sleep(1)


if __name__ == "__main__":
    mapa = mapear_carpetas_locales()
    tn_images = limpiar_tiendanube(mapa)
    limpiar_gumroad(tn_images)
    print("\n" + "=" * 70)
    print("  🎉 ¡LIMPIEZA Y REEMPLAZO 100% COMPLETADOS EN TIENDANUBE Y GUMROAD!")
    print("=" * 70)
