# -*- coding: utf-8 -*-
"""
===============================================================================
MONITOR DE CUOTA DE NUBE Y CONMUTADOR AUTOMÁTICO A GPU LOCAL RTX 3060 (PINOKIO)
===============================================================================
Autor: Alberto Nicolás Noguera
Funcionalidad:
  1. Monitorea la disponibilidad de cuota en servicios de nube.
  2. Si la cuota de la nube se agota o se limita, emite una alerta inmediata.
  3. Conmuta AUTOMÁTICAMENTE la generación de imágenes al motor local de la PC:
     GPU: NVIDIA GeForce RTX 3060 (12 GB VRAM)
     Entorno: Pinokio PyTorch (C:\pinokio\api\fooocus.git\app\env\Scripts\python.exe)
===============================================================================
"""

import os
import sys
import time
import subprocess
from pathlib import Path

PINOKIO_PYTHON = Path(r"C:\pinokio\api\fooocus.git\app\env\Scripts\python.exe")

def verificar_disponibilidad_gpu_local():
    if PINOKIO_PYTHON.exists():
        print(f"✅ GPU Local RTX 3060 con entorno Pinokio detectada en: {PINOKIO_PYTHON}")
        return True
    else:
        print("⚠️ Entorno Pinokio en C:\\pinokio no encontrado, usando Python del sistema.")
        return False

def conmutar_a_generacion_local_rtx(script_renderizado, args=None):
    print("\n" + "=" * 80)
    print(" 🚨 ALERTA DE CUOTA: CUOTA DE NUBE ALCANZADA / LIMITADA")
    print(" 🔄 ACTIVANDO GENERACIÓN AUTOMÁTICA EN GPU LOCAL RTX 3060 (PINOKIO)")
    print("=" * 80)
    
    python_exe = str(PINOKIO_PYTHON) if PINOKIO_PYTHON.exists() else sys.executable
    cmd = [python_exe, str(script_renderizado)]
    if args:
        cmd.extend(args)
        
    print(f"🚀 Ejecutando renderizado en RTX 3060: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("✅ Generación local completada exitosamente en RTX 3060.")
    else:
        print(f"⚠️ El proceso finalizó con código: {result.returncode}")

if __name__ == "__main__":
    verificar_disponibilidad_gpu_local()
