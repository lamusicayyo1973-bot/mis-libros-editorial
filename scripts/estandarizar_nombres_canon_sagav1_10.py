# -*- coding: utf-8 -*-
import sys
import io
import json
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Canonical Replacement Map
replacements = {
    # Antagonist Lord
    r"\bMuzan\b": "Kageyama",
    # Upper Moons
    r"\bKokushibo\b": "Kurogane",
    r"\bDoma\b": "Kagura",
    r"\bAkaza\b": "Rikudo",
    r"\bHantengu\b": "Gomon",
    r"\bGyokko\b": "Gyoshin",
    r"\bRui\b": "Ayane",
    r"\bEnmu\b": "Yumeji",
    # Hashiras / Allies
    r"\bGyomei\b": "Genba",
    r"\bSanemi\b": "Kazuma",
    r"\bMuichiro\b": "Kiri",
    r"\bShinobu\b": "Aoi",
    r"\bKanae\b": "Aoi",
    r"\bMitsuri\b": "Sakura",
    r"\bRengoku\b": "Enma",
    r"\bGiyu\b": "Ryujin",
    r"\bObanai\b": "Hebi",
    r"\bGenya\b": "Tetsuo",
    r"\bKanao\b": "Tsuyu",
    r"\bInosuke\b": "Kiba",
    r"\bZenitsu\b": "Raijin",
    r"\bTanjiro\b": "Ren",
    r"\bNezuko\b": "Miyuki",
    r"\bTamayo\b": "Sumire",
    r"\bYushiro\b": "Renji",
    r"\bYoriichi\b": "Yori"
}

base_dirs = [
    Path(r"C:\Proyectos\mis-libros-editorial\libros"),
    Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros")
]

scripts_dir = Path(r"C:\Proyectos\mis-libros-editorial\scripts")

print("=== REEMPLAZANDO Y ESTANDARIZANDO CANON DE PERSONAJES (VOL 1-10) ===\n")

# 1. Update all ficha_producto.json and scripts
for base in base_dirs:
    if not base.exists():
        continue
    for vol_folder in base.glob("oni-no-ketsuryu-volumen-*"):
        ficha = vol_folder / "ficha_producto.json"
        if ficha.exists():
            content = ficha.read_text(encoding="utf-8")
            for pattern, target in replacements.items():
                content = re.sub(pattern, target, content)
            ficha.write_text(content, encoding="utf-8")
            print(f"  [OK] Estandarizada ficha_producto.json en {vol_folder.name}")

# 2. Update python scripts in scripts_dir
for script_file in scripts_dir.glob("*.py"):
    scontent = script_file.read_text(encoding="utf-8")
    modified = False
    for pattern, target in replacements.items():
        if re.search(pattern, scontent):
            scontent = re.sub(pattern, target, scontent)
            modified = True
    if modified:
        script_file.write_text(scontent, encoding="utf-8")
        print(f"  [OK] Estandarizado script: {script_file.name}")

print("\n¡Canon de personajes estandarizado en todos los archivos!")
