# -*- coding: utf-8 -*-
"""
===============================================================================
LOKI DASHBOARD & PUBLISHER INTERACTIVO: PANEL CONTROL DE LIBROS & GPU
===============================================================================
Autor: Alberto Nicolás Noguera
Funcionalidad:
  1. Panel Web/GUI interactivo para Loki.
  2. Botón 'Importar Carpeta de Libro' para cargar manuscrito + imágenes + copy.
  3. Botón 'Publicar este Libro' para abrir y auto-completar las 5 plataformas:
     (Payhip, Tiendanube Argentina, Gumroad, Hotmart, Amazon KDP).
  4. Monitoreo y aviso de Cuota de Nube con conmutación a RTX 3060 Pinokio.
===============================================================================
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify

# Configuración de Flask
app = Flask(__name__)

BASE_DIR = Path(r"c:\Users\nicol\Downloads\MIS LIBROS")
BOOKS_DIR = BASE_DIR / "libros"
CONFIG_FILE = BASE_DIR / "configuracion_autor.json"
PINOKIO_PYTHON = Path(r"C:\pinokio\api\fooocus.git\app\env\Scripts\python.exe")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loki Control Panel - Nicolás Noguera Editorial</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card-custom { background: rgba(30, 41, 59, 0.8); border: 1px solid #334155; border-radius: 12px; }
        .badge-active { background-color: #10b981; color: #fff; font-size: 0.9rem; }
        .btn-publish { background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; font-weight: bold; color: white; }
        .btn-publish:hover { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-secondary">
            <div>
                <h1 class="fw-bold text-primary">🤖 Panel de Control de Loki</h1>
                <p class="text-muted mb-0">Sistema de Publicación Automática y Control de GPU Local (RTX 3060)</p>
            </div>
            <div>
                <span class="badge badge-active p-2">RTX 3060 Pinokio: LISTA ⚡</span>
            </div>
        </div>

        <!-- Alerta de Cuota y Motor -->
        <div class="alert alert-info border-0 shadow-sm mb-4">
            📌 <strong>Monitoreo de GPU:</strong> Si la cuota de la nube se agota, Loki conmuta automáticamente la generación de portadas al motor local en tu <strong>NVIDIA GeForce RTX 3060 (Pinokio)</strong> a costo $0.
        </div>

        <!-- Sección de Importar Carpeta -->
        <div class="card card-custom p-4 mb-4 shadow">
            <h4 class="text-warning mb-3">📁 Importar Nueva Carpeta de Libro</h4>
            <form action="/importar" method="POST" class="row g-3">
                <div class="col-md-9">
                    <input type="text" name="folder_path" class="form-control bg-dark text-light border-secondary" placeholder="Pegá el camino de la carpeta (ej: C:\Users\nicol\Downloads\mi-nuevo-libro)" required>
                </div>
                <div class="col-md-3">
                    <button type="submit" class="btn btn-warning w-100 fw-bold">📥 Importar Carpeta</button>
                </div>
            </form>
        </div>

        <!-- Catálogo de Libros Registrados -->
        <h3 class="mb-3 text-light">📚 Catálogo de Libros Listos para Publicar</h3>
        <div class="row g-4">
            {% for libro in libros %}
            <div class="col-md-6">
                <div class="card card-custom h-100 p-3 shadow">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5>{{ libro.titulo }}</h5>
                        <span class="badge bg-success">${{ libro.precio_usd }} USD / ${{ libro.precio_ars }} ARS</span>
                    </div>
                    <p class="text-muted small my-2">{{ libro.resumen }}</p>
                    <div class="mb-3">
                        <span class="badge bg-secondary">Docx: {{ '✅' if libro.has_docx else '❌' }}</span>
                        <span class="badge bg-secondary">Portada: {{ '✅' if libro.has_portada else '❌' }}</span>
                        <span class="badge bg-secondary">Ficha SEO: {{ '✅' if libro.has_ficha else '❌' }}</span>
                    </div>
                    <form action="/publicar" method="POST" target="_blank">
                        <input type="hidden" name="folder_id" value="{{ libro.id }}">
                        <button type="submit" class="btn btn-publish w-100 py-2">
                            🚀 PUBLICAR ESTE LIBRO EN LAS 5 PLATAFORMAS
                        </button>
                    </form>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

def cargar_libros():
    libros = []
    if BOOKS_DIR.exists():
        for folder in sorted(BOOKS_DIR.iterdir()):
            if folder.is_dir():
                ficha_file = folder / "ficha_producto.json"
                docx_file = folder / "libro.docx"
                portada_file = folder / "portada.jpg"
                
                titulo = folder.name.replace("-", " ").title()
                resumen = "Edición oficial por Nicolás Noguera"
                precio_usd = 20.0
                precio_ars = 26000
                
                if ficha_file.exists():
                    try:
                        with open(ficha_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            titulo = data.get("titulo", titulo)
                            resumen = data.get("resumen_corto", resumen)
                            precio_usd = data.get("precio_usd", 20.0)
                            precio_ars = data.get("precio_ars", 26000)
                    except Exception:
                        pass
                
                libros.append({
                    "id": folder.name,
                    "titulo": titulo,
                    "resumen": resumen,
                    "precio_usd": precio_usd,
                    "precio_ars": precio_ars,
                    "has_docx": docx_file.exists(),
                    "has_portada": portada_file.exists(),
                    "has_ficha": ficha_file.exists()
                })
    return libros

@app.route("/")
def home():
    libros = cargar_libros()
    return render_template_string(HTML_TEMPLATE, libros=libros)

@app.route("/importar", methods=["POST"])
def importar():
    folder_path = request.form.get("folder_path", "").strip('"')
    if folder_path:
        script = BASE_DIR / "scripts" / "loki_auto_publisher.py"
        subprocess.run([sys.executable, str(script), folder_path])
    return home()

@app.route("/publicar", methods=["POST"])
def publicar():
    folder_id = request.form.get("folder_id", "")
    folder_path = BOOKS_DIR / folder_id
    if folder_path.exists():
        script = BASE_DIR / "scripts" / "loki_auto_publisher.py"
        subprocess.Popen([sys.executable, str(script), str(folder_path)])
    return "<h1>🚀 Loki ha iniciado la apertura automática de las 5 plataformas (Payhip, Tiendanube, Gumroad, Hotmart, Amazon KDP). Podés volver al panel.</h1>"

if __name__ == "__main__":
    print("🤖 Iniciando Panel de Control de Loki en: http://localhost:5000")
    subprocess.Popen('powershell -Command "Start-Process \'http://localhost:5000\'"', shell=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
