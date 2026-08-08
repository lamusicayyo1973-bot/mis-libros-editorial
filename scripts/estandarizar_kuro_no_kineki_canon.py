# -*- coding: utf-8 -*-
import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

scripts_dir = Path(r"C:\Proyectos\mis-libros-editorial\scripts")
base_dirs = [
    Path(r"C:\Proyectos\mis-libros-editorial\libros"),
    Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros")
]

print("=== REVISANDO Y ESTANDARIZANDO LA TRILOGÍA KURO NO KINEKI ===\n")

# In Kuro no Kineki:
# Protagonista: Kael
# Compañera: Sora
# Mentor/Estratega: Marcus
# Reina/Ciudad: Emperatriz Aetheria

replacements_kuro = {
    r"\bRen\b": "Kael",
    r"\bTanjiro\b": "Kael",
    r"\bNezuko\b": "Sora",
    r"\bMuzan\b": "El Ejecutor Oscuro"
}

for script_name in [
    "crear_kuro_no_kineki_docx.py",
    "crear_kuro_no_kineki_vol1_exacto_docx.py",
    "crear_kuro_no_kineki_vol2_docx.py",
    "crear_kuro_no_kineki_vol2_exacto_docx.py",
    "crear_kuro_no_kineki_vol3_docx.py",
    "crear_kuro_no_kineki_vol3_exacto_docx.py",
    "generar_todas_las_escenas_kuro_vol1_rtx.py",
    "generar_todas_las_escenas_kuro_vol2_rtx.py",
    "generar_todas_las_escenas_kuro_vol3_rtx.py"
]:
    sf = scripts_dir / script_name
    if sf.exists():
        content = sf.read_text(encoding="utf-8")
        mod = False
        for pattern, target in replacements_kuro.items():
            if re.search(pattern, content):
                content = re.sub(pattern, target, content)
                mod = True
        if mod:
            sf.write_text(content, encoding="utf-8")
            print(f"  [OK] Estandarizado: {script_name}")

print("\n¡Trilogía Kuro no Kineki estandarizada con éxito!")
