# -*- coding: utf-8 -*-
import sys
import io
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-8")
artifact_dir = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827")

images = [
    ("portada.jpg", "Portada Principal - Demonio marcial Rikudo frente al compás azul de nieve"),
    ("thumbnail.jpg", "Miniatura Cuadrada - Puño marcial con aura de energía azul"),
    ("banner.jpg", "Banner Horizontal - Arena marcial con compás azul brillante"),
    ("escena_1.jpg", "Escena 1 - Ataque Aniquilación de Rikudo con puños de energía"),
    ("escena_c1_e1.jpg", "Capítulo 1 - Escena 1: Ren en estado desprovisto de intención"),
    ("escena_c1_e2.jpg", "Capítulo 1 - Escena 2: Decapitación limpia con la katana solar"),
    ("escena_c1_e3.jpg", "Capítulo 1 - Escena 3: Intento de regeneración del demonio decapitado"),
    ("escena_c2_e1.jpg", "Capítulo 2 - Escena 1: Recuerdos humanos de Hakuji y Koyuki bajo fuegos artificiales"),
    ("escena_c2_e2.jpg", "Capítulo 2 - Escena 2: Redención y desintegración pacífica de Rikudo"),
    ("escena_c2_e3.jpg", "Capítulo 3 - Escena 1: Kagura el Demonio de Hielo consumido por veneno de glicina"),
    ("escena_c3_e1.jpg", "Capítulo 3 - Escena 2: Corte final mariposa cortando el cuello de hielo"),
    ("escena_c3_e2.jpg", "Capítulo 3 - Escena 3: Guerrero jabalí sosteniendo sus katanas dobles"),
    ("escena_c3_e3.jpg", "Capítulo 4 - Escena 1: Pilares de Piedra y Viento enfrentando a Kurogane"),
    ("escena_c4_e1.jpg", "Capítulo 4 - Escena 2: Ráfagas de luna creciente cortando columnas"),
    ("escena_c4_e2.jpg", "Capítulo 4 - Escena 3: Hojas incandescentes al rojo vivo unidas"),
    ("escena_c4_e3.jpg", "Capítulo 4 - Escena 4: Cuatro katanas solares atravesando a Kurogane"),
    ("escena_c5_e1.jpg", "Capítulo 5 - Escena 1: Flauta de madera dejada atrás en la ceniza"),
    ("escena_c5_e2.jpg", "Capítulo 5 - Escena 2: Erupción de Kageyama desde el capullo en los tejados"),
    ("escena_c5_e3.jpg", "Capítulo 5 - Escena 3: Pilares reunidos para la batalla de 90 minutos"),
    ("escena_climax.jpg", "Clímax del Volumen 8 - Erupción del Rey Demonio bajo la luna llena")
]

print("Copiando imágenes del Volumen 8 al directorio de artefactos...")
for filename, desc in images:
    src_file = src_dir / filename
    dest_file = artifact_dir / f"vol8_{filename}"
    if src_file.exists():
        shutil.copy2(src_file, dest_file)
        print(f"  [OK] {filename} -> vol8_{filename}")

# Generate Markdown Artifact content
md_path = artifact_dir / "galeria_volumen_8.md"

md_content = """# 🎨 Galería Completa de Ilustraciones - Oni no Ketsuryū Volumen 8

A continuación podés revisar **las 20 ilustraciones HD una por una** del **Volumen 8 (La Noche de los Noventa Minutos)**. Podés recorrer el carrusel interactivo o ver el listado detallado más abajo.

---

## 🎠 Carrusel de Inspección Imagen por Imagen

````carousel
"""

carousel_slides = []
for filename, desc in images:
    slide = f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol8_{filename})\n\n**{desc}**"
    carousel_slides.append(slide)

md_content += "\n<!-- slide -->\n".join(carousel_slides)
md_content += "\n````\n\n---\n\n## 🖼️ Listado Detallado Una por Una\n\n"

for filename, desc in images:
    md_content += f"### 📌 {desc}\n\n"
    md_content += f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol8_{filename})\n\n"
    md_content += f"*Archivo local:* [`{filename}`](file:///C:/Proyectos/mis-libros-editorial/libros/oni-no-ketsuryu-volumen-8/{filename})\n\n---\n\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print("¡Artefacto galeria_volumen_8.md creado con éxito!")
