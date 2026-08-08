# -*- coding: utf-8 -*-
import sys
import io
import os
import shutil
import sqlite3
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Buscando cookies de sesion activas en Chrome y Edge...")

user_home = Path(os.path.expanduser("~"))
chrome_cookies = user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Network" / "Cookies"
edge_cookies = user_home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Network" / "Cookies"

loki_profile_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")
loki_profile_dir.mkdir(parents=True, exist_ok=True)

# Copy User Data files to loki_browser_profile if possible
chrome_user_data = user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data"
edge_user_data = user_home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data"

target_data = chrome_user_data if chrome_user_data.exists() else edge_user_data

print(f"Detectada fuente de datos de usuario: {target_data}")

# Let's copy Default profile network cookies if accessible
try:
    temp_cookie_db = Path("scratch/temp_cookies.db")
    temp_cookie_db.parent.mkdir(parents=True, exist_ok=True)
    
    src_db = chrome_cookies if chrome_cookies.exists() else edge_cookies
    if src_db.exists():
        shutil.copy2(src_db, temp_cookie_db)
        print(f"Copiada base de cookies desde: {src_db}")
        
        conn = sqlite3.connect(temp_cookie_db)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly FROM cookies WHERE host_key LIKE '%gumroad%' OR host_key LIKE '%hotmart%' OR host_key LIKE '%payhip%' OR host_key LIKE '%amazon%' OR host_key LIKE '%tiendanube%'")
        rows = cursor.fetchall()
        
        found_cookies = {}
        for row in rows:
            domain = row[0]
            name = row[1]
            found_cookies.setdefault(domain, []).append(name)
            
        print(f"Extracto de cookies encontradas: {json.dumps(found_cookies, indent=2)}")
        conn.close()
    else:
        print("No se encontro archivo Cookies en la ruta habitual.")
except Exception as e:
    print(f"Aviso al copiar DB de cookies: {e}")

