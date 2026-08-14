# -*- coding: utf-8 -*-
"""
===============================================================================
CORRECTOR DEFINITIVO - EMPAREJAMIENTO POR TABLA EXPLÍCITA
===============================================================================
Usa una tabla 100% explícita de ID de producto Tiendanube -> carpeta local,
y nombre de producto Gumroad -> carpeta local, sin ninguna ambigüedad.
===============================================================================
"""

import sys
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
BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

tn_headers = {
    "Authentication": f"bearer {TIENDANUBE_TOKEN}",
    "User-Agent": "LokiApp",
    "Content-Type": "application/json"
}

# Tabla explícita: handle de Tiendanube -> nombre de carpeta local
TN_HANDLE_TO_FOLDER = {
    "de-cero-a-negocio-con-ia":                                         "de-cero-a-negocio-con-ia",
    "el-algoritmo-personal":                                            "el-algoritmo-personal",
    "kuro-no-kineki-ecos-de-tinta-negra-volumen-1":                     "kuro-no-kineki-volumen-1",
    "kuro-no-kineki-ecos-de-tinta-negra1":                              "kuro-no-kineki-volumen-2",
    "kuro-no-kineki-ecos-de-tinta-negra2":                              "kuro-no-kineki-volumen-3",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-1-la-noche-de-las-hojas-rotas":                                              "oni-no-ketsuryu-volumen-1",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-10-el-amanecer-del-acero-santo-gran-final-de-saga":                          "oni-no-ketsuryu-volumen-10",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-2-el-examen-de-la-montana-sombria":                                          "oni-no-ketsuryu-volumen-2",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-3-el-tren-de-las-sombras":                                                   "oni-no-ketsuryu-volumen-3",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-4-el-distrito-de-los-espejos-y-la-mariposa-de-la-sombra":                    "oni-no-ketsuryu-volumen-4",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-5-la-aldea-de-los-herreros-olvidados":                                       "oni-no-ketsuryu-volumen-5",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-6-las-catacumbas-del-olvido":                                                "oni-no-ketsuryu-volumen-6",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-7-el-asedio-al-castillo-infinito":                                           "oni-no-ketsuryu-volumen-7",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-8-el-juicio-de-los-tres-demonios-del-abismo":                                "oni-no-ketsuryu-volumen-8",
    "oni-no-ketsuryu-la-estirpe-de-la-sangre-volumen-9-la-noche-de-los-noventa-minutos":                                         "oni-no-ketsuryu-volumen-9",
}

# Tabla explícita: ID de producto Gumroad -> nombre de carpeta local
G_ID_TO_FOLDER = {
    "yGJdbxPZnU3t43ea0gzbiQ==": "oni-no-ketsuryu-volumen-3",
    "DeZkLYoLK26hsqqm3-NWUA==": "oni-no-ketsuryu-volumen-2",
    "Gi8a1mb1fWcRhsOM2wVGQA==": "oni-no-ketsuryu-volumen-10",
    "NBXr7E5GDgT6TrGXDI3a7w==": "oni-no-ketsuryu-volumen-1",
    "pEh-By-DEx8m-D0fV9VpCg==": "kuro-no-kineki-volumen-3",
    "oteY0SYU-noDQ6bDkqIKIg==": "kuro-no-kineki-volumen-2",
    "El6h3YtaS6Hgmy-UMfEM1g==": "kuro-no-kineki-volumen-1",
    "G5voOcYSxe_Q7fmH1-M82w==": "el-algoritmo-personal",
    "5UcckhwTjfp3hsREqq5ZTw==": "de-cero-a-negocio-con-ia",
    "eaDn6TZMy0ttKZ7RDNY47Q==": "de-cero-a-negocio-con-ia",
}


def detectar_carpeta_gumroad(g_id):
    """Retorna la carpeta local por ID exacto de producto Gumroad."""
    return G_ID_TO_FOLDER.get(g_id)


def reparar_tiendanube():
    print("=" * 70)
    print("  [1/2] TIENDANUBE: BORRAR IMAGEN VIEJA + SUBIR PORTADA EXACTA")
    print("=" * 70)

    res = requests.get(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products", headers=tn_headers)
    products = res.json()
    print(f"\n  -> Total: {len(products)} productos\n")

    tn_urls = {}   # folder_name -> URL pública de la nueva imagen

    for idx, p in enumerate(products, 1):
        pid = p.get("id")
        handle_raw = p.get("handle", {})
        handle = handle_raw.get("es", "") if isinstance(handle_raw, dict) else handle_raw
        name_raw = p.get("name", {})
        name = name_raw.get("es", "") if isinstance(name_raw, dict) else name_raw

        folder_name = TN_HANDLE_TO_FOLDER.get(handle)

        print(f"  [{idx:02d}/15] {name[:45]}")
        print(f"         handle: {handle[:50]}")
        print(f"         -> Carpeta: {folder_name or 'NO MAPEADO'}")

        if not folder_name:
            print("         [!] Sin carpeta asignada, omitido")
            continue

        portada = BOOKS_DIR / folder_name / "portada.jpg"
        if not portada.exists():
            print(f"         [!] portada.jpg no encontrada en {folder_name}")
            continue

        # A. Borrar TODAS las imágenes viejas
        for img in p.get("images", []):
            requests.delete(
                f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{pid}/images/{img['id']}",
                headers=tn_headers
            )
            time.sleep(0.2)

        # B. Subir portada.jpg en base64
        with open(portada, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

        r = requests.post(
            f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{pid}/images",
            headers=tn_headers,
            json={"filename": "portada.jpg", "attachment": b64}
        )
        if r.status_code in [200, 201]:
            src = r.json().get("src", "")
            tn_urls[folder_name] = src
            print(f"         [OK] Portada instalada limpia")
        else:
            print(f"         [X] Error {r.status_code}: {r.text[:80]}")

        time.sleep(0.3)

    return tn_urls


def reparar_gumroad(tn_urls):
    print("\n" + "=" * 70)
    print("  [2/2] GUMROAD: BORRAR PORTADAS VIEJAS + ASIGNAR PORTADA EXACTA")
    print("=" * 70)

    g_res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": GUMROAD_TOKEN})
    g_prods = g_res.json().get("products", [])

    print(f"\n  -> Total: {len(g_prods)} productos\n")

    for idx, gp in enumerate(g_prods, 1):
        g_id   = gp.get("id")
        g_name = gp.get("name", "")
        covers = gp.get("covers", [])

        folder_name = detectar_carpeta_gumroad(g_id)
        print(f"  [{idx:02d}/{len(g_prods):02d}] {g_name[:50]}")
        print(f"         -> Carpeta: {folder_name or 'NO DETECTADO'}")

        # A. Borrar TODAS las portadas viejas
        for c in covers:
            requests.delete(
                f"https://api.gumroad.com/v2/products/{g_id}/covers/{c['id']}",
                data={"access_token": GUMROAD_TOKEN}
            )
            time.sleep(0.2)

        # B. Asignar portada correcta
        img_url = tn_urls.get(folder_name) if folder_name else None
        if img_url:
            r = requests.post(
                f"https://api.gumroad.com/v2/products/{g_id}/covers",
                data={"access_token": GUMROAD_TOKEN, "url": img_url}
            )
            if r.status_code == 200:
                print("         [OK] Portada única asignada")
            else:
                print(f"         [X] Error {r.status_code}: {r.text[:80]}")
        else:
            print("         [!] Sin URL de portada disponible")

        time.sleep(0.3)


if __name__ == "__main__":
    tn_urls = reparar_tiendanube()
    reparar_gumroad(tn_urls)
    print("\n" + "=" * 70)
    print("  PROCESO 100% COMPLETADO")
    print("=" * 70)
