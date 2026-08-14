# -*- coding: utf-8 -*-
"""
===============================================================================
LOKI DASHBOARD & PUBLISHER INTERACTIVO: PANEL CONTROL DE LIBROS & GPU
===============================================================================
Autor: Alberto Nicolás Noguera
Funcionalidad:
  1. Panel Web/GUI interactivo para Loki (Port 5000).
  2. Selector Nativo de Carpetas HTML5 (webkitdirectory) + Carga Manual.
  3. API Endpoints completos: /api/ebooks/catalog, /api/ebooks/upload-folder,
     /api/ebooks/import, /api/ebooks/publish.
  4. Publicación simultánea en las 5 plataformas.
===============================================================================
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

current_book_data = {}

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

BASE_DIR = Path(r"C:\Proyectos\mis-libros-editorial")
BOOKS_DIR = BASE_DIR / "libros"
CONFIG_FILE = BASE_DIR / "configuracion_autor.json"

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loki Control Panel - Nicolás Noguera Editorial</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card-custom { background: rgba(30, 41, 59, 0.85); border: 1px solid #334155; border-radius: 14px; }
        .badge-active { background-color: #10b981; color: #fff; font-size: 0.9rem; font-weight: bold; }
        .btn-gold { background: linear-gradient(135deg, #f59e0b, #d97706); border: none; font-weight: 800; color: #000; }
        .btn-gold:hover { background: linear-gradient(135deg, #d97706, #b45309); color: #000; }
        .btn-publish { background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; font-weight: bold; color: white; }
        .btn-publish:hover { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-secondary">
            <div>
                <h1 class="fw-bold text-warning">🤖 Panel de Control de Loki</h1>
                <p class="text-muted mb-0">Sistema de Publicación Automática y Control de GPU Local (NVIDIA RTX 3060 Pinokio)</p>
            </div>
            <div>
                <span class="badge badge-active p-2">⚡ RTX 3060 Pinokio: LISTA</span>
            </div>
        </div>

        <!-- Alerta de Monitoreo -->
        <div class="alert alert-dark border-secondary shadow-sm mb-4">
            📌 <strong>Monitoreo Inteligente:</strong> Si se agota la cuota en la nube, Loki conmuta automáticamente al motor local en tu <strong>RTX 3060 Pinokio</strong> a costo $0.
        </div>

        <!-- Card de Importar Carpeta -->
        <div class="card card-custom p-4 mb-4 shadow border-warning">
            <h4 class="text-warning mb-2">📁 Importar Carpeta de Libro (.docx + imágenes)</h4>
            <p class="text-muted small mb-3">Hacé clic en el botón dorado para seleccionar la carpeta desde tu Explorador de Windows:</p>

            <input type="file" id="native-browser-folder-picker" webkitdirectory directory style="display:none;" onchange="handleBrowserFolderPicked(event)">

            <div class="d-flex gap-2 mb-3">
                <button type="button" class="btn btn-gold btn-lg px-4 shadow-sm" onclick="document.getElementById('native-browser-folder-picker').click()">
                    📁 BUSCAR CARPETA EN MI PC (EXPLORADOR WINDOWS)
                </button>
            </div>

            <div class="input-group">
                <input type="text" id="manual-folder-input" class="form-control bg-dark text-light border-secondary" placeholder="O pegá la ruta manual ej. C:\Users\nicol\Downloads\mi-nuevo-libro">
                <button class="btn btn-outline-light" type="button" onclick="importManualFolder()">📥 Cargar Ruta Tipeada</button>
            </div>
        </div>

        <!-- Catálogo de Libros Registrados -->
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="mb-0 text-light">📚 Catálogo de Libros Registrados</h3>
            <button class="btn btn-sm btn-outline-secondary" onclick="loadCatalogUI()">↺ Refrescar Catálogo</button>
        </div>

        <div class="row g-4" id="books-grid-container">
            <!-- Cargado dinámicamente -->
        </div>
    </div>

    <script>
        async function loadCatalogUI() {
            const container = document.getElementById('books-grid-container');
            container.innerHTML = '<div class="text-muted">Cargando libros del catálogo...</div>';
            try {
                const res = await fetch('/api/ebooks/catalog');
                const data = await res.json();
                if (data.libros && data.libros.length > 0) {
                    container.innerHTML = data.libros.map(l => `
                        <div class="col-md-6">
                            <div class="card card-custom h-100 p-3 shadow">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <h5 class="fw-bold mb-0 text-light">${l.titulo}</h5>
                                    <span class="badge bg-success">$${l.precio_usd} USD / $${l.precio_ars} ARS</span>
                                </div>
                                <p class="text-muted small mb-3">${l.resumen}</p>
                                <div class="mb-3">
                                    <span class="badge bg-secondary">Docx: ${l.has_docx ? '✅' : '❌'}</span>
                                    <span class="badge bg-secondary">Portada: ${l.has_portada ? '✅' : '❌'}</span>
                                    <span class="badge bg-secondary">Ficha SEO: ${l.has_ficha ? '✅' : '❌'}</span>
                                </div>
                                <button onclick="publishEbook('${l.id}')" class="btn btn-publish w-100 py-2 mb-2">
                                    🚀 PUBLICAR ESTE LIBRO EN LAS 5 PLATAFORMAS
                                </button>
                                <button onclick="prepareForExtension('${l.id}', this)" class="btn w-100 py-2" style="background-color: #8b5cf6; color: white; font-weight: 700;">
                                    📝 PREPARAR PARA EXTENSIÓN CHROME
                                </button>
                            </div>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = '<div class="text-muted">No hay libros registrados aún. Hacé clic en el botón dorado arriba para empezar.</div>';
                }
            } catch(e) {
                container.innerHTML = '<div class="text-danger">Error cargando el catálogo de libros.</div>';
            }
        }

        async function handleBrowserFolderPicked(event) {
            const files = event.target.files;
            if (!files || files.length === 0) return;
            
            const relativePath = files[0].webkitRelativePath || '';
            const folderName = relativePath ? relativePath.split('/')[0] : 'libro-importado';
            
            const formData = new FormData();
            formData.append('folder_name', folderName);
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }

            try {
                const res = await fetch('/api/ebooks/upload-folder', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    alert('✅ Carpeta "' + folderName + '" importada exitosamente al catálogo.');
                    loadCatalogUI();
                } else {
                    alert('⚠️ Error al procesar carpeta: ' + (data.message || 'Ocurrió un problema'));
                }
            } catch(e) {
                alert('❌ Error al subir carpeta: ' + e.message);
            }
        }

        async function importManualFolder() {
            const input = document.getElementById('manual-folder-input');
            const path = input ? input.value.trim() : '';
            if (!path) {
                alert('Por favor pegá una ruta de tu computadora.');
                return;
            }
            try {
                const res = await fetch('/api/ebooks/import', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ folder_path: path })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    alert('✅ Carpeta importada exitosamente al catálogo.');
                    input.value = '';
                    loadCatalogUI();
                } else {
                    alert('⚠️ Error: ' + (data.message || 'Ruta no válida'));
                }
            } catch(e) {
                alert('❌ Error de conexión.');
            }
        }

        async function publishEbook(folderId) {
            try {
                const res = await fetch('/api/ebooks/publish', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ folder_id: folderId })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    alert('🚀 Loki ha iniciado la apertura automática de las 5 plataformas (Payhip, Tiendanube, Gumroad, Hotmart, Amazon KDP).');
                } else {
                    alert('⚠️ Error al publicar: ' + data.message);
                }
            } catch(e) {
                alert('❌ Error de conexión al publicar.');
            }
        }

        async function prepareForExtension(folderId, btnEl) {
            console.log('[LOKI] Preparando libro para extensión:', folderId);
            if (btnEl) {
                btnEl.innerText = '⏳ Preparando...';
                btnEl.disabled = true;
            }
            try {
                const res = await fetch('/api/ebooks/set-current', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ folder_id: folderId })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    if (btnEl) {
                        btnEl.innerText = '✅ ¡LISTO! ABRÍ LA EXTENSIÓN EN PAYHIP';
                        btnEl.style.backgroundColor = '#10b981';
                        btnEl.disabled = false;
                    }
                    // Abrir la pestaña de Payhip directamente
                    window.open('https://payhip.com/product/add/digital', '_blank');
                } else {
                    alert('⚠️ Aviso: ' + data.message);
                    if (btnEl) { btnEl.innerText = '📝 PREPARAR PARA EXTENSIÓN CHROME'; btnEl.disabled = false; }
                }
            } catch(e) {
                console.error('[LOKI] Error:', e);
                alert('❌ Error de conexión: ' + e.message);
                if (btnEl) { btnEl.innerText = '📝 PREPARAR PARA EXTENSIÓN CHROME'; btnEl.disabled = false; }
            }
        }

        document.addEventListener('DOMContentLoaded', loadCatalogUI);
    </script>
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/ebooks/catalog', methods=['GET'])
def api_get_catalog():
    return jsonify({"libros": cargar_libros()})

@app.route('/api/ebooks/import', methods=['POST'])
def api_import_folder():
    data = request.get_json(silent=True) or request.form or {}
    folder_raw = data.get("folder_path", "").strip().strip('"').strip("'")
    if not folder_raw:
        return jsonify({"status": "error", "message": "Ruta vacía"}), 400
    
    target_path = Path(folder_raw).resolve()
    if not target_path.exists():
        return jsonify({"status": "error", "message": f"La ruta no existe en la PC: '{target_path}'"}), 400
    
    if target_path.is_file():
        target_path = target_path.parent
        
    script = BASE_DIR / "scripts" / "loki_auto_publisher.py"
    try:
        subprocess.run([sys.executable, str(script), str(target_path)], check=True)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ebooks/upload-folder', methods=['POST'])
def api_upload_folder():
    try:
        folder_name = request.form.get("folder_name", "nuevo-libro").strip()
        folder_slug = "".join(c if c.isalnum() else "-" for c in folder_name.lower()).strip("-")
        if not folder_slug:
            folder_slug = "nuevo-libro"
            
        target_dir = BOOKS_DIR / folder_slug
        target_dir.mkdir(parents=True, exist_ok=True)
        
        uploaded_files = request.files.getlist("files")
        for file_obj in uploaded_files:
            filename = Path(file_obj.filename).name
            if filename:
                file_obj.save(target_dir / filename)
                
        ficha_path = target_dir / "ficha_producto.json"
        if not ficha_path.exists():
            nombre_limpio = folder_name.replace("_", " ").replace("-", " ").title()
            ficha_data = {
                "id": folder_slug,
                "titulo": nombre_limpio,
                "subtitulo": f"Obra oficial por Nicolás Noguera",
                "precio_usd": 20.00,
                "precio_ars": 26000,
                "resumen_corto": f"Edición digital oficial de {nombre_limpio} por Nicolás Noguera."
            }
            with open(ficha_path, "w", encoding="utf-8") as f:
                json.dump(ficha_data, f, indent=4, ensure_ascii=False)
                
        return jsonify({"status": "ok", "folder": folder_slug})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ebooks/publish', methods=['POST'])
def api_publish_platforms():
    data = request.get_json(silent=True) or request.form or {}
    folder_id = data.get("folder_id", "")
    folder_path = BOOKS_DIR / folder_id
    if not folder_path.exists():
        return jsonify({"status": "error", "message": "Carpeta de libro no encontrada"}), 404
    
    script = BASE_DIR / "scripts" / "loki_auto_publisher.py"
    try:
        subprocess.Popen([sys.executable, str(script), str(folder_path)])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ebooks/current', methods=['GET'])
def api_get_current():
    if not current_book_data:
        return jsonify({"status": "empty", "message": "Ningun libro seleccionado"}), 404
    return jsonify({"status": "ok", "libro": current_book_data})

@app.route('/api/ebooks/set-current', methods=['POST'])
def api_set_current():
    global current_book_data
    data = request.get_json(silent=True) or request.form or {}
    folder_id = data.get('folder_id', '')
    folder_path = BOOKS_DIR / folder_id
    ficha_file = folder_path / 'ficha_producto.json'
    if not ficha_file.exists():
        return jsonify({'status': 'error', 'message': 'No existe ficha_producto.json'}), 404
    
    with open(ficha_file, 'r', encoding='utf-8') as f:
        ficha = json.load(f)
    
    ficha['folder_id'] = folder_id
    current_book_data = ficha
    
    # Abrir la carpeta en el Explorador de Windows
    try:
        os.startfile(str(folder_path))
    except Exception as e:
        print("[LOKI] Error al abrir explorador:", e)

    return jsonify({'status': 'ok', 'libro': ficha})

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        sys.stdout.reconfigure(encoding='utf-8')
    print("[EDITORIAL] Iniciando Panel Editorial en: http://localhost:5100")
    app.run(host="0.0.0.0", port=5100, debug=False)
