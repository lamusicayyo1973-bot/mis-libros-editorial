# -*- coding: utf-8 -*-
import sys
import io
import json
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros")

kuro_folders = [
    base_dir / "kuro-no-kineki-volumen-1",
    base_dir / "kuro-no-kineki-volumen-2",
    base_dir / "kuro-no-kineki-volumen-3"
]

print("=== AUDITORÍA DE PERSONAJES EN LA TRILOGÍA KURO NO KINEKI (VOL 1, 2 Y 3) ===\n")

for folder in kuro_folders:
    print(f"📌 {folder.name}:")
    ficha = folder / "ficha_producto.json"
    if ficha.exists():
        data = json.loads(ficha.read_text(encoding="utf-8"))
        print(f"   Título: {data.get('titulo')}")
        print(f"   Headline: {data.get('headline')}")
        print(f"   Descripción: {data.get('descripcion')}\n")
    else:
        print("   ❌ No se encontró ficha_producto.json\n")

