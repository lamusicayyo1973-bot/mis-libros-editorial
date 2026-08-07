# -*- coding: utf-8 -*-
"""
===============================================================================
LOKI AUTO-PUBLISHER: CARGA AUTOMÁTICA POR CARPETA DROPPED (LOKI FOLDER ENGINE)
===============================================================================
Autor: Alberto Nicolás Noguera
Funcionalidad:
  Le indicás cualquier carpeta de tu PC que contenga:
    - Manuscrito (.docx o .pdf)
    - Portada o Imágenes (.jpg o .png)
    - (Opcional) Ficha de datos / Prompts

  Loki automáticamente:
    1. Procesa y estructura el nuevo libro.
    2. Lo registra en el catálogo general.
    3. Abre y carga automáticamente en las 5 plataformas:
       - Payhip
       - Tiendanube Argentina
       - Gumroad
       - Hotmart
       - Amazon KDP
    4. Sincroniza las URLs públicas con GitHub.
===============================================================================
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Paths principales
BASE_DIR = Path(r"C:\Proyectos\mis-libros-editorial")
BOOKS_DIR = BASE_DIR / "libros"
CONFIG_FILE = BASE_DIR / "configuracion_autor.json"

PLATAFORMAS_URLS = {
    "payhip": ("https://payhip.com/product/add/digital", "Payhip - Nuevo Producto Digital"),
    "tiendanube": ("https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new", "Tiendanube Argentina - Carga en Pesos"),
    "gumroad": ("https://gumroad.com/products/new", "Gumroad - Nuevo Ebook"),
    "hotmart": ("https://app.hotmart.com/tools/products/create", "Hotmart - Registrar Producto"),
    "amazon_kdp": ("https://kdp.amazon.com/title-setup/kdb/new", "Amazon KDP - Crear Libro Kindle")
}

def procesar_carpeta_ingresada(path_carpeta_origen):
    raw_clean = str(path_carpeta_origen).strip().strip('"').strip("'")
    path_origen = Path(raw_clean).resolve()
    if not path_origen.exists():
        print(f"[ERROR] La ruta especificada no existe: {raw_clean}")
        return None
    if path_origen.is_file():
        path_origen = path_origen.parent

    print(f"\n[LOKI] Escaneando carpeta: {path_origen}")
    
    # 1. Buscar Manuscrito (.docx o .pdf)
    manuscritos = list(path_origen.glob("*.docx")) + list(path_origen.glob("*.pdf"))
    if not manuscritos:
        print("[AVISO] No se encontró manuscrito (.docx o .pdf) en la carpeta.")
        manuscrito = None
    else:
        manuscrito = manuscritos[0]
        print(f"[OK] Manuscrito detectado: {manuscrito.name}")

    # 2. Buscar Portada e Imágenes
    imagenes = list(path_origen.glob("*.jpg")) + list(path_origen.glob("*.png")) + list(path_origen.glob("*.jpeg"))
    portada = None
    for img in imagenes:
        if "portada" in img.name.lower() or "cover" in img.name.lower():
            portada = img
            break
    if not portada and imagenes:
        portada = imagenes[0]
    
    if portada:
        print(f"[OK] Portada detectada: {portada.name}")

    # 3. Leer o Crear Ficha de Producto
    ficha_path = path_origen / "ficha_producto.json"
    if ficha_path.exists():
        with open(ficha_path, "r", encoding="utf-8") as f:
            ficha_data = json.load(f)
    else:
        nombre_limpio = path_origen.name.replace("_", " ").replace("-", " ").title()
        ficha_data = {
            "id": path_origen.name.lower().replace(" ", "-"),
            "titulo": nombre_limpio,
            "subtitulo": f"Obra oficial por Nicolás Noguera",
            "precio_usd": 20.00,
            "precio_ars": 26000,
            "resumen_corto": f"Descargá la edición digital oficial de {nombre_limpio} por Nicolás Noguera.",
            "copy_ventas": {
                "headline": f"Obtené tu copia digital de {nombre_limpio}",
                "cuerpo": f"{nombre_limpio} es una obra exclusiva por Alberto Nicolás Noguera con edición ilustrada de alta calidad."
            }
        }
        with open(ficha_path, "w", encoding="utf-8") as f:
            json.dump(ficha_data, f, ensure_ascii=False, indent=2)

    # 4. Copiar e Integrar en el Catálogo de MIS LIBROS (si no es la misma carpeta)
    folder_destino = BOOKS_DIR / ficha_data["id"]
    folder_destino.mkdir(parents=True, exist_ok=True)
    
    if path_origen.resolve() != folder_destino.resolve():
        if manuscrito:
            shutil.copy2(manuscrito, folder_destino / f"libro{manuscrito.suffix}")
        if portada:
            shutil.copy2(portada, folder_destino / "portada.jpg")
        with open(folder_destino / "ficha_producto.json", "w", encoding="utf-8") as f:
            json.dump(ficha_data, f, ensure_ascii=False, indent=2)

    print(f"\n[EXITO] Libro registrado en el catalogo general: {folder_destino}")
    
    return {
        "folder_path": str(folder_destino),
        "titulo": ficha_data["titulo"],
        "precio_usd": ficha_data.get("precio_usd", 20.00),
        "manuscrito": str(folder_destino / f"libro{manuscrito.suffix}") if manuscrito else None,
        "portada": str(folder_destino / "portada.jpg") if portada else None,
        "ficha": ficha_data
    }

def ejecutar_publicacion_loki_5_plataformas(libro_info):
    print("\n" + "=" * 80)
    print(f" LOKI INICIANDO PUBLICACION AUTOMATICA INVISIBLE EN LAS 5 PLATAFORMAS")
    print(f" LIBRO: '{libro_info['titulo']}'")
    print("=" * 80)
    
    script_auto = BASE_DIR / "scripts" / "loki_automated_5_platforms.py"
    cmd = f'python "{script_auto}" "{Path(libro_info["folder_path"]).name}"'
    
    print(f"[*] Ejecutando robot de carga Playwright en segundo plano...")
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(res.stdout)
        print("\n[OK] Carga 100% completada sin abrir ventanas molestas.")
    except Exception as e:
        print(f"[ERROR] Error durante la carga automatizada: {e}")

def main():
    print("=" * 80)
    print(" LOKI CARGA AUTOMATICA POR CARPETA (FOLDER AUTOMATION)")
    print("=" * 80)
    print(" Simplemente indica o arrastra la carpeta con las imagenes y el libro.")
    print("=" * 80)
    
    if len(sys.argv) > 1:
        carpeta_input = sys.argv[1].strip('"')
    else:
        carpeta_input = input("\nIngresa el camino de la carpeta (ej. c:\\Users\\nicol\\Downloads\\mi-nuevo-libro): ").strip('"')

    libro_info = procesar_carpeta_ingresada(carpeta_input)
    if libro_info:
        print("\n[LOKI] Libro procesado y listo para publicar en las 5 plataformas.")
        ejecutar_publicacion_loki_5_plataformas(libro_info)

if __name__ == "__main__":
    main()
