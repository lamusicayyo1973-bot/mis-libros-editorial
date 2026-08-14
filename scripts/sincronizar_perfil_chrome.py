# -*- coding: utf-8 -*-
import sys
import io
import os
import shutil
import sqlite3
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

user_home = Path(os.path.expanduser("~"))
chrome_dir = user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default"
loki_profile_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")
loki_default_dir = loki_profile_dir / "Default"
loki_default_dir.mkdir(parents=True, exist_ok=True)

print("Sincronizando datos de sesion de Chrome con el perfil de automatización Loki...")

# Copy Cookies and Local Storage from Chrome to loki_browser_profile
files_to_sync = [
    ("Network/Cookies", "Network/Cookies"),
    ("Web Data", "Web Data"),
    ("Login Data", "Login Data")
]

for src_rel, dst_rel in files_to_sync:
    src_file = chrome_dir / src_rel
    dst_file = loki_default_dir / dst_rel
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    
    if src_file.exists():
        try:
            shutil.copy2(src_file, dst_file)
            print(f"  [OK] Sincronizado: {src_rel}")
        except Exception as e:
            # If locked by open Chrome, copy via Volume shadow / temp read
            print(f"  [Aviso] {src_rel} en uso por Chrome. Copiando en modo lectura compartida...")
            try:
                with open(src_file, "rb") as f_in:
                    content = f_in.read()
                with open(dst_file, "wb") as f_out:
                    f_out.write(content)
                print(f"  [OK] Copiado exitoso en modo lectura: {src_rel}")
            except Exception as e2:
                print(f"  [Error] No se pudo copiar {src_rel}: {e2}")

print("\n¡Perfil de automatización Loki listo con tus sesiones cargadas!")
