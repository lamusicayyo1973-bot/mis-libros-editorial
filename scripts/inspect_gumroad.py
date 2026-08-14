# -*- coding: utf-8 -*-
import sys
import requests

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

GUMROAD_TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"

res = requests.get("https://api.gumroad.com/v2/products", params={"access_token": GUMROAD_TOKEN})
prods = res.json().get("products", [])

print(f"Total productos en Gumroad: {len(prods)}\n")
for idx, p in enumerate(prods, 1):
    pid = p.get("id")
    name = p.get("name")
    covers = p.get("covers", [])
    print(f"{idx}. ID: {pid} | Nombre: {name}")
    print(f"   Covers: {len(covers)} | Url: {p.get('short_url')}")
    if covers:
        print(f"   Cover URL: {covers[0].get('url')}")
    print("-" * 60)
