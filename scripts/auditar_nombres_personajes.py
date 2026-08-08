# -*- coding: utf-8 -*-
import sys
import io
import json
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros")

# List of Demon Slayer / external manga trademarked names to check
trademark_names = [
    "Kageyama", "Rikudo", "Kurogane", "Kagura", "Genba", "Kazuma", "Kiri", 
    "Aoi", "Aoi", "Ren", "Miyuki", "Tsuyu", "Kiba", "Raijin", 
    "Enma", "Ryujin", "Sakura", "Hebi", "Tetsuo", "Yori", "Michikatsu", 
    "Kaigaku", "Ayane", "Yumeji", "Gyoshin", "Gomon", "Nakime", "Sumire", "Renji"
]

print("=== AUDITORÍA COMPLETA DE NOMBRES EN TODOS LOS VOLÚMENES (1 AL 10) ===\n")

findings = {}

for vol_folder in sorted(base_dir.glob("oni-no-ketsuryu-volumen-*")):
    vol_name = vol_folder.name
    findings[vol_name] = []
    
    # Check ficha_producto.json
    ficha_path = vol_folder / "ficha_producto.json"
    if ficha_path.exists():
        content = ficha_path.read_text(encoding="utf-8")
        for tname in trademark_names:
            matches = re.findall(rf"\b{tname}\b", content, re.IGNORECASE)
            if matches:
                findings[vol_name].append(f"ficha_producto.json: {tname} (x{len(matches)})")
                
    # Check creation script if exists
    vol_num = vol_name.split("-")[-1]
    script_path = Path(rf"C:\Proyectos\mis-libros-editorial\scripts\crear_oni_no_ketsuryu_vol{vol_num}_docx.py")
    if script_path.exists():
        scontent = script_path.read_text(encoding="utf-8")
        for tname in trademark_names:
            matches = re.findall(rf"\b{tname}\b", scontent, re.IGNORECASE)
            if matches:
                findings[vol_name].append(f"script vol{vol_num}: {tname} (x{len(matches)})")

for vol_name, matches in findings.items():
    if matches:
        print(f"❌ {vol_name}:")
        for m in matches:
            print(f"   - {m}")
    else:
        print(f"✅ {vol_name}: Limpio de nombres externos")

print("\nAuditoría finalizada.")
