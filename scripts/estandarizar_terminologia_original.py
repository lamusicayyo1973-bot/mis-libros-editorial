# -*- coding: utf-8 -*-
import sys
import io
import json
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Dictionary of terms to replace with original lore
term_replacements = {
    # Hierarchy replacements
    r"\bPilares\b": "Maestros Celestiales",
    r"\bPilar\b": "Maestro Celestial",
    r"\bHashira\b": "Sables de Elite",
    r"\bLunares Superiores\b": "Demonios del Abismo",
    r"\bLunar Superior\b": "Demonio del Abismo",
    r"\bLunares Rojos\b": "Estirpes de Sangre",
    r"\bLunar Rojo\b": "Estirpe de Sangre",
    r"\bLunar\b": "Estirpe",
    r"\bRespiración del Sol\b": "Estilo de Dominio Solar",
    r"\bRespiración de la Niebla\b": "Estilo de la Niebla Helada",
    r"\bRespiración del Viento\b": "Estilo del Viento Cortante",
    r"\bRespiración de la Flor\b": "Estilo de la Flor Mortal",
    r"\bRespiración de la Piedra\b": "Estilo de la Piedra Ancestral",
    r"\bRespiración del Fuego\b": "Estilo del Fuego Carmesí",
    r"\bRespiración\b": "Estilo de Esgrima",
    r"\bCazadores de Demonios\b": "Hermandad del Sol",
    r"\bCazadores\b": "Guerreros de la Hermandad",
    r"\bCazador\b": "Guerrero de la Hermandad",
    r"\bMarca del Guerrero de la Hermandad\b": "Sello de Sangre Solar"
}

base_dirs = [
    Path(r"C:\Proyectos\mis-libros-editorial\libros"),
    Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros")
]

scripts_dir = Path(r"C:\Proyectos\mis-libros-editorial\scripts")

print("=== REEMPLAZANDO TERMINOLOGÍA POR CONCEPTOS 100% ORIGINALES (VOL 1-10) ===\n")

for base in base_dirs:
    if not base.exists():
        continue
    for vol_folder in base.glob("oni-no-ketsuryu-volumen-*"):
        ficha = vol_folder / "ficha_producto.json"
        if ficha.exists():
            content = ficha.read_text(encoding="utf-8")
            for pattern, target in term_replacements.items():
                content = re.sub(pattern, target, content)
            ficha.write_text(content, encoding="utf-8")
            print(f"  [OK] Terminología actualizada en ficha_producto.json ({vol_folder.name})")

for script_file in scripts_dir.glob("*.py"):
    scontent = script_file.read_text(encoding="utf-8")
    modified = False
    for pattern, target in term_replacements.items():
        if re.search(pattern, scontent):
            scontent = re.sub(pattern, target, scontent)
            modified = True
    if modified:
        script_file.write_text(scontent, encoding="utf-8")
        print(f"  [OK] Terminología actualizada en script: {script_file.name}")

print("\n¡Terminología 100% original aplicada en todos los archivos!")
