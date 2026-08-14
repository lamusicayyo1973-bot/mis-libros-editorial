# -*- coding: utf-8 -*-
import sys
import io
import json
import requests
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ACCESS_TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"
BASE_URL = "https://api.gumroad.com/v2"
BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

# Todos los libros del catálogo
BOOKS = [
    "el-algoritmo-personal",
    "de-cero-a-negocio-con-ia",
    "kuro-no-kineki-volumen-1",
    "kuro-no-kineki-volumen-2",
    "kuro-no-kineki-volumen-3",
    "oni-no-ketsuryu-volumen-1",
    "oni-no-ketsuryu-volumen-2",
    "oni-no-ketsuryu-volumen-3",
    "oni-no-ketsuryu-volumen-4",
    "oni-no-ketsuryu-volumen-5",
    "oni-no-ketsuryu-volumen-6",
    "oni-no-ketsuryu-volumen-7",
    "oni-no-ketsuryu-volumen-8",
    "oni-no-ketsuryu-volumen-9",
    "oni-no-ketsuryu-volumen-10",
]

results = []

for book_id in BOOKS:
    book_folder = BOOKS_DIR / book_id
    ficha_file = book_folder / "ficha_producto.json"

    if not ficha_file.exists():
        print(f"  [!] Sin ficha_producto.json: {book_id}")
        continue

    with open(ficha_file, "r", encoding="utf-8") as f:
        ficha = json.load(f)

    titulo = ficha.get("titulo", book_id)
    subtitulo = ficha.get("subtitulo", "")
    nombre_completo = f"{titulo}: {subtitulo}" if subtitulo else titulo
    precio_usd = ficha.get("precio_usd", ficha.get("precio", 20.00))
    precio_centavos = int(float(precio_usd) * 100)

    copy = ficha.get("copy_ventas", {})
    descripcion = f"{copy.get('headline', '')}\n\n{copy.get('cuerpo', '')}"
    if not descripcion.strip():
        descripcion = ficha.get("resumen_corto", nombre_completo)

    print(f"\n[+] Subiendo a Gumroad: {nombre_completo}")
    print(f"    Precio: ${precio_usd} USD ({precio_centavos} centavos)")

    # 1. Crear el producto
    payload = {
        "access_token": ACCESS_TOKEN,
        "name": nombre_completo,
        "price": precio_centavos,
        "description": descripcion,
        "currency": "usd",
    }

    resp = requests.post(f"{BASE_URL}/products", data=payload)
    data = resp.json()

    if not data.get("success"):
        print(f"    [X] Error al crear producto: {data.get('message', data)}")
        results.append({"book": book_id, "status": "ERROR", "msg": str(data)})
        continue

    product_id = data["product"]["id"]
    product_url = data["product"].get("short_url", "")
    print(f"    [✓] Producto creado! ID: {product_id}")
    print(f"    [✓] URL: {product_url}")

    # 2. Subir archivo .docx
    docx_file = book_folder / "libro.docx"
    if docx_file.exists():
        with open(docx_file, "rb") as df:
            file_resp = requests.put(
                f"{BASE_URL}/products/{product_id}/enable",
                data={"access_token": ACCESS_TOKEN}
            )
        # Upload file via multipart
        with open(docx_file, "rb") as df:
            file_upload_resp = requests.post(
                f"{BASE_URL}/products/{product_id}/product_files",
                data={"access_token": ACCESS_TOKEN},
                files={"file": (docx_file.name, df, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            )
        file_data = file_upload_resp.json()
        if file_data.get("success"):
            print(f"    [✓] Manuscrito .docx subido correctamente")
        else:
            print(f"    [!] Aviso al subir .docx: {file_data.get('message', file_data)}")

    # 3. Subir portada
    portada_file = book_folder / "portada.jpg"
    if portada_file.exists():
        with open(portada_file, "rb") as pf:
            cover_resp = requests.post(
                f"{BASE_URL}/products/{product_id}/product_files",
                data={"access_token": ACCESS_TOKEN},
                files={"file": (portada_file.name, pf, "image/jpeg")}
            )
        cover_data = cover_resp.json()
        if cover_data.get("success"):
            print(f"    [✓] Portada subida correctamente")
        else:
            print(f"    [!] Aviso al subir portada: {cover_data.get('message', cover_data)}")

    results.append({
        "book": book_id,
        "titulo": nombre_completo,
        "status": "OK",
        "product_id": product_id,
        "url": product_url
    })

# Guardar resumen
resumen_file = Path(r"C:\Proyectos\mis-libros-editorial\gumroad_upload_results.json")
with open(resumen_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("✅ CARGA COMPLETA EN GUMROAD")
print("="*60)
ok = [r for r in results if r.get("status") == "OK"]
err = [r for r in results if r.get("status") != "OK"]
print(f"  Publicados exitosamente: {len(ok)}")
print(f"  Errores: {len(err)}")
for r in ok:
    print(f"  ✓ {r['titulo'][:60]} → {r.get('url')}")
for r in err:
    print(f"  ✗ {r['book']} → {r.get('msg','')[:80]}")
print(f"\nResumen guardado en: {resumen_file}")
