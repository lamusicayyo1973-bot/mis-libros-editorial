# -*- coding: utf-8 -*-
import sys
import io
import os
import shutil
import win32file
import win32con
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

user_home = Path(os.path.expanduser("~"))
chrome_cookies = user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Network" / "Cookies"

loki_profile_dir = Path(r"C:\Proyectos\loki\automation\loki_browser_profile")
loki_network_dir = loki_profile_dir / "Default" / "Network"
loki_network_dir.mkdir(parents=True, exist_ok=True)
dst_cookies = loki_network_dir / "Cookies"

print("Copiando cookies de sesion activas de Chrome usando pywin32 shared read...")

try:
    # Open file with share read/write/delete permissions
    handle = win32file.CreateFile(
        str(chrome_cookies),
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL,
        None
    )
    
    # Read bytes
    rc, data = win32file.ReadFile(handle, os.path.getsize(chrome_cookies))
    win32file.CloseHandle(handle)
    
    # Write to destination
    with open(dst_cookies, "wb") as f:
        f.write(data)
        
    print(f"¡Exito! Copiadas {len(data)} bytes de cookies a {dst_cookies}")
except Exception as e:
    print(f"Aviso al copiar cookies con pywin32: {e}")
