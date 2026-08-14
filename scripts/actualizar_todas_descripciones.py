# -*- coding: utf-8 -*-
"""
===============================================================================
ACTUALIZADOR COMPLETO DE DESCRIPCIONES EN TIENDANUBE Y GUMROAD
===============================================================================
Lee la ficha_producto.json de cada libro y sube la descripción rica en HTML 
(con Sinopsis, Beneficios e Índice de Capítulos) a Tiendanube y Gumroad.
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

BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")
TN_TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
TN_STORE = "8063094"
G_TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"

tn_headers = {
    "Authentication": f"bearer {TN_TOKEN}",
    "User-Agent": "LokiApp",
    "Content-Type": "application/json"
}

# Tabla de mapeo Tiendanube: handle -> carpeta local
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

# Tabla de mapeo Gumroad: ID -> carpeta local
G_ID_TO_FOLDER = {
    "yGJdbxPZnU3t43ea0gzbiQ==": "oni-no-ketsuryu-volumen-3",
    "DeZkLYoLK26hsqqm3-NWUA==": "oni-no-ketsuryu-volumen-2",
    "Gi8a1mb1fWcRhsOM2wVGQA==": "oni-no-ketsuryu-volumen-4",
    "NBXr7E5GDgT6TrGXDI3a7w==": "oni-no-ketsuryu-volumen-1",
    "pEh-By-DEx8m-D0fV9VpCg==": "kuro-no-kineki-volumen-3",
    "oteY0SYU-noDQ6bDkqIKIg==": "kuro-no-kineki-volumen-2",
    "El6h3YtaS6Hgmy-UMfEM1g==": "kuro-no-kineki-volumen-1",
    "G5voOcYSxe_Q7fmH1-M82w==": "el-algoritmo-personal",
    "5UcckhwTjfp3hsREqq5ZTw==": "de-cero-a-negocio-con-ia",
    "eaDn6TZMy0ttKZ7RDNY47Q==": "de-cero-a-negocio-con-ia",
}


def armar_html_descripcion(ficha):
    """Construye un HTML elegante y vendedor para Tiendanube/Gumroad."""
    headline    = ficha.get("headline", "")
    desc        = ficha.get("descripcion", "")
    beneficios  = ficha.get("beneficios", [])
    capitulos   = ficha.get("capitulos", [])
    autor       = ficha.get("autor", "Nicolás Noguera")

    html = []
    if headline:
        html.append(f"<p><strong>✨ {headline}</strong></p><hr>")
    if desc:
        html.append(f"<h3>📖 Sinopsis</h3><p>{desc}</p>")

    if beneficios:
        html.append("<h3>✨ Lo que incluye este eBook</h3><ul>")
        for b in beneficios:
            html.append(f"<li>{b}</li>")
        html.append("</ul>")

    if capitulos:
        html.append("<h3>📑 Contenido y Capítulos</h3><ul>")
        for c in capitulos:
            html.append(f"<li>{c}</li>")
        html.append("</ul>")

    html.append(f"<br><p><strong>Autor:</strong> {autor}<br><strong>Editorial:</strong> Nicolás Noguera Editorial</p>")
    return "\n".join(html)


def actualizar_tiendanube():
    print("=" * 70)
    print("  [1/2] ACTUALIZANDO DESCRIPCIONES EN TIENDANUBE")
    print("=" * 70)

    res = requests.get(f"https://api.tiendanube.com/v1/{TN_STORE}/products", headers=tn_headers, params={"per_page": 50})
    products = res.json()

    for idx, p in enumerate(products, 1):
        pid = p.get("id")
        handle_raw = p.get("handle", {})
        handle = handle_raw.get("es", "") if isinstance(handle_raw, dict) else handle_raw
        name_raw = p.get("name", {})
        name = name_raw.get("es", "") if isinstance(name_raw, dict) else name_raw

        folder = TN_HANDLE_TO_FOLDER.get(handle)
        print(f"\n[{idx:02d}/15] {name[:50]}")

        if not folder:
            print("   [!] Carpeta no mapeada")
            continue

        ficha_path = BOOKS_DIR / folder / "ficha_producto.json"
        if not ficha_path.exists():
            print("   [!] Ficha no encontrada")
            continue

        with open(ficha_path, encoding="utf-8") as f:
            ficha = json.load(f)

        desc_html = armar_html_descripcion(ficha)

        r = requests.put(
            f"https://api.tiendanube.com/v1/{TN_STORE}/products/{pid}",
            headers=tn_headers,
            json={"description": {"es": desc_html}}
        )
        if r.status_code == 200:
            print(f"   [OK] Descripción actualizada en Tiendanube ({len(desc_html)} caracteres)")
        else:
            print(f"   [X] Error {r.status_code}: {r.text[:80]}")

        time.sleep(0.3)


def actualizar_gumroad():
    print("\n" + "=" * 70)
    print("  [2/2] ACTUALIZANDO DESCRIPCIONES EN GUMROAD")
    print("=" * 70)

    g_res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": G_TOKEN}).json()
    g_prods = g_res.get("products", [])

    for idx, gp in enumerate(g_prods, 1):
        g_id   = gp.get("id")
        g_name = gp.get("name", "")

        folder = G_ID_TO_FOLDER.get(g_id)
        print(f"\n[{idx:02d}/{len(g_prods):02d}] {g_name[:50]}")

        if not folder:
            print("   [!] Carpeta no mapeada")
            continue

        ficha_path = BOOKS_DIR / folder / "ficha_producto.json"
        if not ficha_path.exists():
            print("   [!] Ficha no encontrada")
            continue

        with open(ficha_path, encoding="utf-8") as f:
            ficha = json.load(f)

        desc_html = armar_html_descripcion(ficha)

        r = requests.put(
            f"https://api.gumroad.com/v2/products/{g_id}",
            data={
                "access_token": G_TOKEN,
                "description": desc_html
            }
        )
        if r.status_code == 200:
            print(f"   [OK] Descripción actualizada en Gumroad ({len(desc_html)} caracteres)")
        else:
            print(f"   [X] Error {r.status_code}: {r.text[:80]}")

        time.sleep(0.3)


if __name__ == "__main__":
    actualizar_tiendanube()
    actualizar_gumroad()
    print("\n" + "=" * 70)
    print("  ¡TODAS LAS DESCRIPCIONES FUERON ACTUALIZADAS Y ENRIQUECIDAS!")
    print("=" * 70)
