# -*- coding: utf-8 -*-
import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

scripts_dir = Path(r"C:\Proyectos\mis-libros-editorial\scripts")

kuro_scripts = [
    scripts_dir / "generar_todas_las_escenas_kuro_vol1_rtx.py",
    scripts_dir / "generar_todas_las_escenas_kuro_vol2_rtx.py",
    scripts_dir / "generar_todas_las_escenas_kuro_vol3_rtx.py"
]

docx_scripts = [
    scripts_dir / "crear_kuro_no_kineki_vol1_exacto_docx.py",
    scripts_dir / "crear_kuro_no_kineki_vol2_exacto_docx.py",
    scripts_dir / "crear_kuro_no_kineki_vol3_exacto_docx.py"
]

print("=== AUDITORÍA DETALLADA DE PERSONAJES EN LA TRILOGÍA KURO NO KINEKI ===\n")

for script in kuro_scripts + docx_scripts:
    if script.exists():
        content = script.read_text(encoding="utf-8")
        print(f"📄 Script: {script.name}")
        # Find capital words/names
        names_found = set(re.findall(r"\b[A-Z][a-z]{2,}\b", content))
        # Filter out python keywords
        ignore = {"Anime", "Style", "Dark", "Fantasy", "Chapter", "Volumen", "Volume", "Masterpiece", "High", "Quality", "Japan", "Feudal", "Japanese", "True", "False", "None", "Path", "Inches", "Pt", "RGBColor", "Document", "Georgia", "Path", "Title", "Synopsis", "Generated", "Saved", "Error"}
        character_candidates = [n for n in names_found if n not in ignore]
        print(f"   Personajes / Nombres detectados: {sorted(character_candidates)}\n")
