# -*- coding: utf-8 -*-
import sys
import io
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-7")
artifact_dir = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827")

images = [
    ("portada.jpg", "Portada Principal - Héroe saltando en el laberinto flotante del Castillo Infinito"),
    ("thumbnail.jpg", "Miniatura Cuadrada - Kagura el Demonio de Hielo con abanicos de loto dorados"),
    ("banner.jpg", "Banner Horizontal - Arquitectura del Castillo Infinito con habitaciones flotantes"),
    ("escena_1.jpg", "Escena 1 - Caída de los cazadores en el abismo del Castillo Infinito"),
    ("escena_c1_e1.jpg", "Capítulo 1 - Escena 1: Aoi la Sables de Elite Mariposa en vigas flotantes"),
    ("escena_c1_e2.jpg", "Capítulo 1 - Escena 2: Kagura el Demonio de Hielo sonriendo en pétalos de loto"),
    ("escena_c1_e3.jpg", "Capítulo 1 - Escena 3: Ataque relámpago con veneno de mariposa"),
    ("escena_c2_e1.jpg", "Capítulo 2 - Escena 1: Estatuas de buda de cristal helado en la sala de hielo"),
    ("escena_c2_e2.jpg", "Capítulo 2 - Escena 2: El sacrificio del veneno de glicina"),
    ("escena_c2_e3.jpg", "Capítulo 2 - Escena 3: Decapitación del Demonio de Hielo"),
    ("escena_c3_e1.jpg", "Capítulo 3 - Escena 1: Genba el Maestro Celestial de la Piedra y Kazuma el Maestro Celestial del Viento"),
    ("escena_c3_e2.jpg", "Capítulo 3 - Escena 2: Kurogane desenfundando su espada de carne y ojos"),
    ("escena_c3_e3.jpg", "Capítulo 3 - Escena 3: Kiri clavado al pilar activando su marca"),
    ("escena_c4_e1.jpg", "Capítulo 4 - Escena 1: Choque de la bola de picos de hierro contra ráfagas de luna"),
    ("escena_c4_e2.jpg", "Capítulo 4 - Escena 2: Ataque combinado de tornado de viento y dragón solar"),
    ("escena_c4_e3.jpg", "Capítulo 4 - Escena 3: Transformación monstruosa de Kurogane"),
    ("escena_c5_e1.jpg", "Capítulo 5 - Escena 1: Los cazadores atravesando el pecho de Kurogane con luz solar"),
    ("escena_c5_e2.jpg", "Capítulo 5 - Escena 2: El recuerdo trágico del hermano gemelo al atardecer"),
    ("escena_c5_e3.jpg", "Capítulo 5 - Escena 3: Colapso del Castillo Infinito elevándose hacia la superficie"),
    ("escena_climax.jpg", "Clímax del Volumen 7 - Desintegración de Kurogane tras la batalla")
]

print("Copiando imágenes del Volumen 7 al directorio de artefactos...")
for filename, desc in images:
    src_file = src_dir / filename
    dest_file = artifact_dir / f"vol7_{filename}"
    if src_file.exists():
        shutil.copy2(src_file, dest_file)
        print(f"  [OK] {filename} -> vol7_{filename}")

# Generate Markdown Artifact content
md_path = artifact_dir / "galeria_volumen_7.md"

md_content = """# 🎨 Galería Completa de Ilustraciones - Oni no Ketsuryū Volumen 7

A continuación podés revisar **las 20 ilustraciones HD una por una** del **Volumen 7 (El Asedio al Castillo Infinito)**. Podés recorrer el carrusel interactivo o ver el listado detallado más abajo.

---

## 🎠 Carrusel de Inspección Imagen por Imagen

````carousel
"""

carousel_slides = []
for filename, desc in images:
    slide = f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol7_{filename})\n\n**{desc}**"
    carousel_slides.append(slide)

md_content += "\n<!-- slide -->\n".join(carousel_slides)
md_content += "\n````\n\n---\n\n## 🖼️ Listado Detallado Una por Una\n\n"

for filename, desc in images:
    md_content += f"### 📌 {desc}\n\n"
    md_content += f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol7_{filename})\n\n"
    md_content += f"*Archivo local:* [`{filename}`](file:///C:/Proyectos/mis-libros-editorial/libros/oni-no-ketsuryu-volumen-7/{filename})\n\n---\n\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print("¡Artefacto galeria_volumen_7.md creado con éxito!")
