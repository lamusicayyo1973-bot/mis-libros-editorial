import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

TOKEN = "jwui9PWifxu0A7O-TaBMKvlpNaIBi-NcjK5-0eBfSfI"
g = requests.get('https://api.gumroad.com/v2/products', params={'access_token': TOKEN}).json()
for i, p in enumerate(g.get('products', [])):
    covers = p.get('covers', [])
    covers_urls = [c.get('original_url', c.get('url', '?'))[:80] for c in covers]
    print(f"{i+1}. [{p['id']}] {p['name'][:60]}")
    if covers_urls:
        for u in covers_urls:
            print(f"   IMG: {u}")
    else:
        print(f"   IMG: (sin portada)")
    print()
