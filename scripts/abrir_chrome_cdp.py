# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import asyncio
from pathlib import Path

# Launch standard Chrome with remote debugging enabled on port 9222
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

print(f"Lanzando Chrome con puerto de automatizacion CDP 9222: {chrome_path}")

cmd = [
    chrome_path,
    "--remote-debugging-port=9222",
    "--start-maximized"
]

subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
print("¡Chrome lanzado en modo automatización CDP!")
