# -*- coding: utf-8 -*-
import sys
import io
import os
import sqlite3
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_path = Path(r"C:\Users\nicol\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies")
dest_path = Path(r"C:\Proyectos\mis-libros-editorial\scratch\Cookies.db")
dest_path.parent.mkdir(parents=True, exist_ok=True)

# Copy locked file using Python binary read
try:
    with open(src_path, "rb") as f_in:
        data = f_in.read()
    with open(dest_path, "wb") as f_out:
        f_out.write(data)
    print("Base de datos Cookies copiada con éxito!")
    
    conn = sqlite3.connect(dest_path)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, path FROM cookies WHERE host_key LIKE '%gumroad%' OR host_key LIKE '%hotmart%' OR host_key LIKE '%payhip%' OR host_key LIKE '%amazon%' OR host_key LIKE '%tiendanube%'")
    rows = cursor.fetchall()
    
    summary = {}
    for host, name, path in rows:
        summary.setdefault(host, []).append(name)
        
    print("Summary of active session cookies found in your Chrome profile:")
    print(json.dumps(summary, indent=2))
    conn.close()
except Exception as e:
    print("Error leyendo DB de cookies:", e)
