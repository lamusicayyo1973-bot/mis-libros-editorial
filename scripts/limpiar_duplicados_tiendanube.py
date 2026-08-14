# -*- coding: utf-8 -*-
import sys
import json
import requests

TIENDANUBE_TOKEN = "229c3f089e44f7e80c71e7508140327e2ced2cee"
TIENDANUBE_STORE_ID = "8063094"

headers = {
    "Authentication": f"bearer {TIENDANUBE_TOKEN}",
    "User-Agent": "LokiApp"
}

def eliminar_duplicados_tiendanube():
    print("=" * 70)
    print("  ELIMINANDO DUPLICADOS EN TIENDANUBE")
    print("=" * 70)

    duplicados = [
        ("360186703", "DE CERO A NEGOCIO CON IA (Duplicado)"),
        ("360186749", "EL ALGORITMO PERSONAL (Duplicado)")
    ]

    for prod_id, nombre in duplicados:
        url = f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{prod_id}"
        r = requests.delete(url, headers=headers)
        if r.status_code == 200:
            print(f"  [OK] Eliminado duplicado: {nombre} (ID: {prod_id})")
        else:
            print(f"  [!] Estado al eliminar {nombre}: {r.status_code}")

    kuro_updates = [
        ("360186789", "KURO NO KINEKI (Ecos de Tinta Negra) - Volumen 1"),
        ("360186816", "KURO NO KINEKI (Ecos de Tinta Negra) - Volumen 2"),
        ("360186861", "KURO NO KINEKI (Ecos de Tinta Negra) - Volumen 3")
    ]

    print("\n  Actualizando titulos de la saga Kuro no Kineki...")
    for prod_id, nuevo_titulo in kuro_updates:
        url = f"https://api.tiendanube.com/v1/{TIENDANUBE_STORE_ID}/products/{prod_id}"
        r = requests.put(url, headers=headers, json={"name": {"es": nuevo_titulo}})
        if r.status_code == 200:
            print(f"  [OK] Titulo actualizado a: {nuevo_titulo}")

    print("\n" + "=" * 70)
    print("  PROCESO COMPLETADO EN TIENDANUBE")
    print("=" * 70)

if __name__ == "__main__":
    eliminar_duplicados_tiendanube()
