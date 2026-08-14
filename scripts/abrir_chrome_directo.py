# -*- coding: utf-8 -*-
import sys
import os
import subprocess
from pathlib import Path

profile_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")
profile_dir.mkdir(parents=True, exist_ok=True)

urls = [
    "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new",
    "https://payhip.com/product/add/digital",
    "https://gumroad.com/products/new",
    "https://app.hotmart.com/tools/products/create",
    "https://kdp.amazon.com/"
]

# Find Chrome or Edge executable on Windows
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

exe_found = None
for p in chrome_paths:
    if os.path.exists(p):
        exe_found = p
        break

if not exe_found:
    print("No se encontró Chrome ni Edge en la ruta estándar. Abriendo con navegador por defecto...")
    for u in urls:
        os.system(f'start "" "{u}"')
else:
    print(f"Encontrado navegador nativo: {exe_found}")
    print(f"Abriendo perfil persistente en: {profile_dir}")
    
    # Launch Chrome directly on Windows Desktop with the persistent profile
    cmd = [
        exe_found,
        f"--user-data-dir={profile_dir}",
        "--start-maximized"
    ] + urls
    
    subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    print("¡Proceso de Chrome lanzado exitosamente en tu escritorio Windows!")
