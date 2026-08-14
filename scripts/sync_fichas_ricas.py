# -*- coding: utf-8 -*-
import json
from pathlib import Path

base_src = Path(r"C:\Proyectos\mis-libros-editorial\sistema_editorial\libros")
base_dst = Path(r"C:\Proyectos\mis-libros-editorial\libros")

# 1. Sync de-cero-a-negocio-con-ia
with open(base_src / 'de-cero-a-negocio-con-ia' / 'ficha_producto.json', encoding='utf-8') as f:
    f_src = json.load(f)
f_dst = {
    'titulo': 'DE CERO A NEGOCIO CON IA: Cómo lanzar y ejecutar tu emprendimiento en 90 días',
    'autor': 'Nicolás Noguera',
    'precio': 20.0,
    'headline': f_src.get('copy_ventas', {}).get('headline', ''),
    'descripcion': f_src.get('copy_ventas', {}).get('cuerpo', ''),
    'beneficios': f_src.get('puntos_clave', []),
    'capitulos': [f"{m.get('titulo','')}: {m.get('capitulos','')}".strip(": ") for m in f_src.get('copy_ventas', {}).get('modulos', [])]
}
with open(base_dst / 'de-cero-a-negocio-con-ia' / 'ficha_producto.json', 'w', encoding='utf-8') as f:
    json.dump(f_dst, f, ensure_ascii=False, indent=2)

# 2. Sync el-algoritmo-personal
with open(base_src / 'el-algoritmo-personal' / 'ficha_producto.json', encoding='utf-8') as f:
    f_src = json.load(f)
f_dst = {
    'titulo': 'EL ALGORITMO PERSONAL: Rediseñá tus hábitos, dominá tu enfoque y ejecutá con claridad',
    'autor': 'Nicolás Noguera',
    'precio': 20.0,
    'headline': f_src.get('copy_ventas', {}).get('headline', ''),
    'descripcion': f_src.get('copy_ventas', {}).get('cuerpo', ''),
    'beneficios': f_src.get('puntos_clave', []),
    'capitulos': [f"{m.get('titulo','')}: {m.get('capitulos','')}".strip(": ") for m in f_src.get('copy_ventas', {}).get('modulos', [])]
}
with open(base_dst / 'el-algoritmo-personal' / 'ficha_producto.json', 'w', encoding='utf-8') as f:
    json.dump(f_dst, f, ensure_ascii=False, indent=2)

# 3. Sync Kuro 1, 2, 3
for i in [1, 2, 3]:
    folder_name = f'kuro-no-kineki-volumen-{i}'
    with open(base_src / folder_name / 'ficha_producto.json', encoding='utf-8') as f:
        f_src = json.load(f)
    f_dst = {
        'titulo': f_src.get('titulo', f'Kuro no Kineki - Volumen {i}'),
        'autor': 'Nicolás Noguera',
        'precio': 20.0,
        'headline': f_src.get('copy_ventas', {}).get('headline', f_src.get('resumen_corto', '')),
        'descripcion': f_src.get('copy_ventas', {}).get('cuerpo', f_src.get('resumen_corto', '')),
        'beneficios': f_src.get('puntos_clave', []),
        'capitulos': [f"{m.get('titulo','')}".strip() for m in f_src.get('copy_ventas', {}).get('modulos', []) if m.get('titulo')]
    }
    with open(base_dst / folder_name / 'ficha_producto.json', 'w', encoding='utf-8') as f:
        json.dump(f_dst, f, ensure_ascii=False, indent=2)

print('Rich marketing copy synced successfully!')
