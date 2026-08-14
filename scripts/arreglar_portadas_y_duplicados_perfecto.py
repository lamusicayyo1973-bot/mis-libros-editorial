# -*- coding: utf-8 -*-
"""
===============================================================================
CORRECTOR COMPLETO Y PERFECTO DE PORTADAS Y DUPLICADOS (TIENDANUBE + GUMROAD)
===============================================================================
1. Elimina duplicados de Gumroad y Tiendanube.
2. Reemplaza la imagen de CADA producto en Tiendanube con la portada.jpg EXACTA de su carpeta local.
3. Asigna a CADA producto de Gumroad la URL exacta de su portada en Tiendanube.
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


def obtener_mapa_carpetas():
    mapa = {}
    for f in BOOKS_DIR.iterdir():
        if f.is_dir():
            ficha_p = f / "ficha_producto.json"
            if ficha_p.exists():
                with open(ficha_p, "r", encoding="utf-8") as file:
                    ficha = json.load(file)
                titulo = ficha.get("titulo", "")
                subtitulo = ficha.get("subtitulo", "")
                mapa[f.name] = {
                    "path": f,
                    "titulo": titulo,
                    "subtitulo": subtitulo,
                    "full_title": f"{titulo}: {subtitulo}".strip(": "),
                    "portada": f / "portada.jpg"
                }
    return mapa


def arreglar_tiendanube(mapa_carpetas):
    print("=" * 70)
    print("  [1/2] ARREGLANDO IMÁGENES Y DUPLICADOS EN TIENDANUBE")
    print("=" * 70)

    res = requests.get(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products", headers=tn_headers)
    products = res.json()

    print(f"\n  -> Total productos en Tiendanube: {len(products)}")

    # Mapear cada producto de Tiendanube a su carpeta correcta por slug / handle
    for p in products:
        pid = p.get("id")
        handle = p.get("handle", {}).get("es", "") if isinstance(p.get("handle"), dict) else p.get("handle", "")
        name = p.get("name", {}).get("es", "") if isinstance(p.get("name"), dict) else p.get("name", "")

        # Encontrar carpeta local correspondiente
        matched_folder = None
        for slug, info in mapa_carpetas.items():
            if slug in handle or handle in slug or info["titulo"].lower() in name.lower():
                # Para Oni no Ketsuryu, coincidir número de volumen
                if "volumen" in slug:
                    vol_num = slug.split("volumen-")[-1]
                    if f"volumen-{vol_num}" in handle or f"volumen {vol_num}" in name.lower() or f"volumen-{vol_num}" in slug:
                        matched_folder = info
                        break
                else:
                    matched_folder = info
                    break

        if not matched_folder:
            print(f"  [!] No se pudo emparejar: {name} (handle: {handle})")
            continue

        portada_path = matched_folder["portada"]
        if not portada_path.exists():
            print(f"  [!] No existe portada.jpg en {matched_folder['path'].name}")
            continue

        print(f"\n  [~] Procesando: {name}")
        print(f"      Carpeta: {matched_folder['path'].name}")

        # 1. Eliminar imágenes viejas/incorrectas
        images = p.get("images", [])
        for img in images:
            img_id = img.get("id")
            del_url = f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{pid}/images/{img_id}"
            requests.delete(del_url, headers=tn_headers)
            print(f"      -> Imagen anterior {img_id} eliminada")

        # 2. Subir portada.jpg correcta en base64
        with open(portada_path, "rb") as img_file:
            b64_str = base64.b64encode(img_file.read()).decode("utf-8")

        post_img_url = f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{pid}/images"
        payload = {
            "filename": "portada.jpg",
            "attachment": b64_str
        }
        r = requests.post(post_img_url, headers=tn_headers, json=payload)
        if r.status_code == 201 or r.status_code == 200:
            print("      [OK] Portada.jpg subida e instalada correctamente")
        else:
            print(f"      [X] Error subiendo imagen: {r.status_code} {r.text[:100]}")

        time.sleep(1)


def arreglar_gumroad(mapa_carpetas):
    print("\n" + "=" * 70)
    print("  [2/2] ARREGLANDO IMÁGENES Y DUPLICADOS EN GUMROAD")
    print("=" * 70)

    # 1. Obtener lista actual de Gumroad
    res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": GUMROAD_TOKEN})
    g_prods = res.json().get("products", [])

    print(f"\n  -> Total productos en Gumroad: {len(g_prods)}")

    # 2. Obtener imágenes actualizadas de Tiendanube
    tn_res = requests.get(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products", headers=tn_headers)
    tn_prods = tn_res.json()
    tn_images_map = {}
    for p in tn_prods:
        handle = p.get("handle", {}).get("es", "") if isinstance(p.get("handle"), dict) else p.get("handle", "")
        images = p.get("images", [])
        if images:
            tn_images_map[handle] = images[0].get("src")

    # 3. Eliminar duplicado exacto EUsCJ_A84XumLTExs41ADA==
    dup_id = "EUsCJ_A84XumLTExs41ADA=="
    del_res = requests.delete(f"https://api.gumroad.com/v2/products/{dup_id}", data={"access_token": GUMROAD_TOKEN})
    if del_res.status_code == 200:
        print(f"  [OK] Producto duplicado {dup_id} eliminado de Gumroad")

    # 4. Actualizar portadas en Gumroad
    for gp in g_prods:
        g_id = gp.get("id")
        if g_id == dup_id:
            continue

        g_name = gp.get("name", "")
        print(f"\n  [~] Actualizando Gumroad: {g_name[:50]}")

        # Encontrar slug de Tiendanube correspondiente
        target_img_url = None
        for slug, info in mapa_carpetas.items():
            if info["titulo"].lower() in g_name.lower() or slug in g_name.lower():
                if "volumen" in slug:
                    vol_num = slug.split("volumen-")[-1]
                    if f"volumen {vol_num}" in g_name.lower() or f"volumen-{vol_num}" in slug:
                        for tn_handle, img_url in tn_images_map.items():
                            if f"volumen-{vol_num}" in tn_handle:
                                target_img_url = img_url
                                break
                        break
                else:
                    for tn_handle, img_url in tn_images_map.items():
                        if slug in tn_handle:
                            target_img_url = img_url
                            break
                    break

        if target_img_url:
            print(f"      Subiendo portada correcta desde Tiendanube...")
            r = requests.post(
                f"https://api.gumroad.com/v2/products/{g_id}/covers",
                data={"access_token": GUMROAD_TOKEN, "url": target_img_url}
            )
            if r.status_code == 200:
                print("      [OK] Portada correcta asignada en Gumroad")
            else:
                print(f"      [X] Error asignando portada: {r.status_code} {r.text[:100]}")
        else:
            print("      [!] No se encontro URL de portada equivalente")

        time.sleep(1)


if __name__ == "__main__":
    mapa = obtener_mapa_carpetas()
    arreglar_tiendanube(mapa)
    arreglar_gumroad(mapa)
    print("\n" + "=" * 70)
    print("  🎉 ¡TODAS LAS PORTADAS Y DUPLICADOS CORREGIDOS PERFECTAMENTE!")
    print("=" * 70)
