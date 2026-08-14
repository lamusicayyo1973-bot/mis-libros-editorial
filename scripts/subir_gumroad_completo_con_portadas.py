# -*- coding: utf-8 -*-
import sys, json, requests
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ACCESS_TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"
BASE_URL = "https://api.gumroad.com/v2"
BOOKS_DIR = Path(r"C:\Proyectos\mis-libros-editorial\libros")

REMAINING_BOOKS = [
    "oni-no-ketsuryu-volumen-5",
    "oni-no-ketsuryu-volumen-6",
    "oni-no-ketsuryu-volumen-7",
    "oni-no-ketsuryu-volumen-8",
    "oni-no-ketsuryu-volumen-9",
    "oni-no-ketsuryu-volumen-10"
]

def subir_faltantes_a_gumroad():
    print("=== INICIANDO SUBIDA DE LIBROS FALTANTES A GUMROAD ===")
    
    for book_id in REMAINING_BOOKS:
        folder = BOOKS_DIR / book_id
        ficha_file = folder / "ficha_producto.json"
        if not ficha_file.exists():
            continue

        with open(ficha_file, "r", encoding="utf-8") as f:
            ficha = json.load(f)

        titulo = ficha.get("titulo", book_id)
        subtitulo = ficha.get("subtitulo", "")
        nombre_completo = f"{titulo}: {subtitulo}" if subtitulo else titulo
        precio_usd = ficha.get("precio_usd", ficha.get("precio", 20.00))
        precio_centavos = int(float(precio_usd) * 100)

        descripcion = ficha.get("descripcion", "") or ficha.get("headline", "")
        beneficios = "\n".join([f"• {b}" for b in ficha.get("beneficios", [])])
        desc_final = f"{descripcion}\n\nIncluye:\n{beneficios}\n\nEdición digital oficial de Nicolás Noguera Editorial."

        print(f"\n[+] Subiendo a Gumroad: {nombre_completo}")

        payload = {
            "access_token": ACCESS_TOKEN,
            "name": nombre_completo,
            "price": precio_centavos,
            "description": desc_final,
            "currency": "usd"
        }

        # 1. Crear producto
        resp = requests.post(f"{BASE_URL}/products", data=payload)
        data = resp.json()

        if not data.get("success"):
            print(f"    [!] Error al crear en Gumroad: {data.get('message', data)}")
            continue

        product_id = data["product"]["id"]
        short_url = data["product"].get("short_url", "")
        print(f"    [✓] Creado! ID: {product_id} | URL: {short_url}")

        # 2. Subir Portada
        portada_file = folder / "portada.jpg"
        if portada_file.exists():
            with open(portada_file, "rb") as pf:
                cov_res = requests.post(
                    f"{BASE_URL}/products/{product_id}/product_files",
                    data={"access_token": ACCESS_TOKEN},
                    files={"file": (portada_file.name, pf, "image/jpeg")}
                )
            print("    [✓] Portada enviada a Gumroad.")

        # 3. Subir Manuscrito PDF / DOCX
        pdf_file = folder / "libro.pdf"
        docx_file = folder / "libro.docx"
        file_to_upload = pdf_file if pdf_file.exists() else docx_file
        if file_to_upload.exists():
            with open(file_to_upload, "rb") as df:
                f_type = "application/pdf" if file_to_upload.suffix == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                requests.post(
                    f"{BASE_URL}/products/{product_id}/product_files",
                    data={"access_token": ACCESS_TOKEN},
                    files={"file": (file_to_upload.name, df, f_type)}
                )
            print(f"    [✓] Archivo descargable ({file_to_upload.name}) adjunto.")

        # 4. Publicar producto
        requests.put(f"{BASE_URL}/products/{product_id}/enable", data={"access_token": ACCESS_TOKEN})
        print(f"    [✓] Producto publicado y activo en Gumroad!")

if __name__ == "__main__":
    subir_faltantes_a_gumroad()
