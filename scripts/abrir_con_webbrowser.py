# -*- coding: utf-8 -*-
import sys
import io
import time
import webbrowser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

urls = [
    ("Tiendanube", "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new"),
    ("Payhip", "https://payhip.com/product/add/digital"),
    ("Gumroad", "https://gumroad.com/products/new"),
    ("Hotmart", "https://app.hotmart.com/tools/products/create"),
    ("Amazon KDP", "https://kdp.amazon.com/")
]

print("Abriendo las 5 plataformas de venta en tu navegador web por defecto con Python...")

for name, url in urls:
    print(f"  [+] Abriendo {name}: {url}")
    webbrowser.open(url)
    time.sleep(1)

print("\n¡Las 5 pestañas han sido enviadas a tu navegador web!")
