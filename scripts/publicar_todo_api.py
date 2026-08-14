# -*- coding: utf-8 -*-
"""
===============================================================================
PUBLICADOR MASIVO VÍA API CON DETECCIÓN DE DUPLICADOS (DEDUPLICACIÓN)
===============================================================================
Autor: Alberto Nicolás Noguera

Obtiene primero la lista de productos ya creados en Gumroad y Tiendanube.
Solo publica los libros que NO hayan sido publicados previamente.
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

BASE_DIR = Path(r"C:\Proyectos\mis-libros-editorial")
BOOKS_DIR = BASE_DIR / "libros"

GUMROAD_TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"
TIENDANUBE_TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
TIENDANUBE_STORE_ID = "8063094"

sys.path.insert(0, str(BASE_DIR / "scripts"))
from loki_auto_publisher import publicar_gumroad_api, publicar_tiendanube_api, actualizar_pagina_web_local


def normalizar_texto(txt):
    if not txt:
        return ""
    txt = txt.lower()
    for c in [":", "-", "_", "•", "  ", "volumen", "vol"]:
        txt = txt.replace(c, " ")
    return " ".join(txt.split())


def obtener_titulos_gumroad():
    titulos = set()
    try:
        res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": GUMROAD_TOKEN})
        data = res.json()
        if data.get("success"):
            for p in data.get("products", []):
                titulos.add(normalizar_texto(p.get("name", "")))
    except Exception as e:
        print(f"  [!] Error consultando Gumroad: {e}")
    return titulos


def obtener_titulos_tiendanube():
    titulos = set()
    try:
        headers = {
            "Authentication": f"bearer {TIENDANUBE_TOKEN}",
            "User-Agent": "LokiEditorial (nicolas@noguera.com)"
        }
        res = requests.get(f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products", headers=headers)
        if res.status_code == 200:
            for p in res.json():
                nombre_es = p.get("name", {}).get("es", "") if isinstance(p.get("name"), dict) else p.get("name", "")
                titulos.add(normalizar_texto(nombre_es))
    except Exception as e:
        print(f"  [!] Error consultando Tiendanube: {e}")
    return titulos


def publicar_inteligente_api():
    print("=" * 70)
    print("  🚀 PUBLICACIÓN INTELIGENTE VÍA API (CON DEDUPLICACIÓN)")
    print("=" * 70)

    print("\n  [1/3] Verificando catálogo existente en Gumroad...")
    gumroad_existentes = obtener_titulos_gumroad()
    print(f"        -> {len(gumroad_existentes)} productos ya en Gumroad.")

    print("\n  [2/3] Verificando catálogo existente en Tiendanube...")
    tiendanube_existentes = obtener_titulos_tiendanube()
    print(f"        -> {len(tiendanube_existentes)} productos ya en Tiendanube.")

    libros = sorted([f for f in BOOKS_DIR.iterdir() if f.is_dir()])
    total = len(libros)
    print(f"\n  [3/3] Procesando {total} libros de la editorial:\n")

    reporte = []

    for idx, folder in enumerate(libros, 1):
        ficha_file = folder / "ficha_producto.json"
        if not ficha_file.exists():
            continue

        with open(ficha_file, "r", encoding="utf-8") as f:
            ficha = json.load(f)

        titulo = ficha.get("titulo", folder.name)
        norm_t = normalizar_texto(titulo)

        print(f"  -------------------------------------------------------------")
        print(f"  [{idx}/{total}] LIBRO: {titulo}")

        # 1. Gumroad
        ya_en_gumroad = any(norm_t in g or g in norm_t for g in gumroad_existentes)
        if ya_en_gumroad:
            print("        [✓] Gumroad: Ya publicado anteriormente (OMITIDO)")
            url_g = "Ya publicado"
        else:
            try:
                url_g = publicar_gumroad_api(ficha, folder)
            except Exception as e:
                url_g = f"Error: {e}"

        # 2. Tiendanube
        ya_en_tiendanube = any(norm_t in t or t in norm_t for t in tiendanube_existentes)
        if ya_en_tiendanube:
            print("        [✓] Tiendanube: Ya publicado anteriormente (OMITIDO)")
            url_t = "Ya publicado"
        else:
            try:
                url_t = publicar_tiendanube_api(ficha, folder)
            except Exception as e:
                url_t = f"Error: {e}"

        # 3. Tu Web
        try:
            actualizar_pagina_web_local(ficha, folder)
            print("        [✓] Tu Web: Catálogo web actualizado localmente")
        except Exception as e:
            print(f"        [X] Tu Web Error: {e}")

        reporte.append({
            "titulo": titulo,
            "gumroad": url_g,
            "tiendanube": url_t
        })

        time.sleep(0.5)

    print("\n" + "=" * 70)
    print("  🎉 PROCESO FINALIZADO CON ÉXITO")
    print("=" * 70)
    print("\n  RESUMEN FINAL:\n")
    for item in reporte:
        print(f"  • {item['titulo']}")
        print(f"    - Gumroad:    {item['gumroad']}")
        print(f"    - Tiendanube: {item['tiendanube']}")
        print()


if __name__ == "__main__":
    publicar_inteligente_api()
