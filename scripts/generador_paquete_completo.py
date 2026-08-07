# -*- coding: utf-8 -*-
"""
===============================================================================
GENERADOR DE PAQUETE COMPLETO DE EBOOK PARA LOKI (LOKI BUNDLE CREATOR)
===============================================================================
Autor: Alberto Nicolás Noguera
Funcionalidad:
  Ensambla la carpeta 100% completa de cualquier libro para que Loki pueda
  subirlo automáticamente a las 5 plataformas (Payhip, Tiendanube, Gumroad,
  Hotmart, Amazon KDP).

Archivos incluidos en el paquete:
  1. libro.docx (Manuscrito formateado nativo)
  2. libro.pdf (Edición PDF)
  3. portada.jpg (Portada 8k)
  4. banner.jpg (Banner publicitario)
  5. thumbnail.jpg (Miniatura cuadrada)
  6. imagenes/ (Carpeta con las 15 escenas ilustradas)
  7. ficha_producto.json (Metadatos completísimos: SEO, Copy, Precios USD/ARS)
===============================================================================
"""

import os
import sys
import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"c:\Users\nicol\Downloads\MIS LIBROS")
BOOKS_DIR = BASE_DIR / "libros"

def crear_paquete_completo_libro(id_libro, titulo, subtitulo, resumen, copy_ventas, precio_usd=20.0, precio_ars=26000):
    folder_libro = BOOKS_DIR / id_libro
    folder_libro.mkdir(parents=True, exist_ok=True)
    (folder_libro / "imagenes").mkdir(exist_ok=True)

    ficha = {
        "id": id_libro,
        "titulo": titulo,
        "subtitulo": subtitulo,
        "autor": "Alberto Nicolás Noguera",
        "autor_portada": "NICOLÁS NOGUERA",
        "cuil_dni": "20-23524683-0",
        "cbu_banco_provincia": "0140017503401755100235",
        "precio_usd": precio_usd,
        "precio_ars": precio_ars,
        "resumen_corto": resumen,
        "copy_ventas": copy_ventas,
        "archivos": {
            "manuscrito_docx": "libro.docx",
            "manuscrito_pdf": "libro.pdf",
            "portada": "portada.jpg",
            "banner": "banner.jpg",
            "thumbnail": "thumbnail.jpg",
            "carpeta_escenas": "imagenes/"
        },
        "seo": {
            "marca": "Nicolás Noguera Editorial",
            "tags": ["ebook", "manga", "ia", "emprendimiento", "nicolas noguera"],
            "titulo_seo": f"{titulo} - Edición Oficial por Nicolás Noguera",
            "descripcion_seo": f"{resumen[:150]}"
        }
    }

    ficha_file = folder_libro / "ficha_producto.json"
    with open(ficha_file, "w", encoding="utf-8") as f:
        json.dump(ficha, f, ensure_ascii=False, indent=2)

    print(f"✅ Paquete oficial creado en: {folder_libro}")
    return folder_libro

if __name__ == "__main__":
    print("Paquete listo para ensamblado de libros.")
