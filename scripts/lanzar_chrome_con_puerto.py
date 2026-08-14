# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import time
from pathlib import Path

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_exe):
    chrome_exe = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

profile_dir = Path(r"C:\Proyectos\loki\automation\chrome_cdp_profile")
profile_dir.mkdir(parents=True, exist_ok=True)

urls = [
    "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new",
    "https://payhip.com/product/add/digital",
    "https://gumroad.com/products/new",
    "https://app.hotmart.com/tools/products/create"
]

print(f"Lanzando Chrome independiente con CDP 9222 y perfil propio en: {profile_dir}")

cmd = [
    chrome_exe,
    "--remote-debugging-port=9222",
    f"--user-data-dir={profile_dir}",
    "--start-maximized"
] + urls

subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
print("¡Chrome independiente con puerto 9222 lanzado exitosamente!")
