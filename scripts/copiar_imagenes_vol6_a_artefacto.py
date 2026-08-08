# -*- coding: utf-8 -*-
import sys
import io
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-6")
artifact_dir = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827")

images = [
    ("portada.jpg", "Portada Principal - Kurogane el Demonio de los Seis Ojos en las catacumbas"),
    ("thumbnail.jpg", "Miniatura Cuadrada - Samurai con marca del sol bajo flores de glicina"),
    ("banner.jpg", "Banner Horizontal - Santuario de flores de glicina de noche"),
    ("escena_1.jpg", "Escena 1 - Llegada al santuario sagrado de glicinas"),
    ("escena_c1_e1.jpg", "Capítulo 1 - Escena 1: Reunión de los Maestros Celestiales Sables de Elite en sala de tatami"),
    ("escena_c1_e2.jpg", "Capítulo 1 - Escena 2: Entrenamiento esquivando rocas gigantes"),
    ("escena_c1_e3.jpg", "Capítulo 1 - Escena 3: Meditación bajo cascada helada"),
    ("escena_c2_e1.jpg", "Capítulo 2 - Escena 1: Descenso a las catacumbas subterráneas"),
    ("escena_c2_e2.jpg", "Capítulo 2 - Escena 2: Altar antiguo con runas solares"),
    ("escena_c2_e3.jpg", "Capítulo 2 - Escena 3: Sombra con seis ojos rojos en las sombras"),
    ("escena_c3_e1.jpg", "Capítulo 3 - Escena 1: Kurogane desenfundando katana de carne"),
    ("escena_c3_e2.jpg", "Capítulo 3 - Escena 2: Choque de espadas luna vs sol"),
    ("escena_c3_e3.jpg", "Capítulo 3 - Escena 3: Visión transparente viendo venas del enemigo"),
    ("escena_c4_e1.jpg", "Capítulo 4 - Escena 1: Afilado de la hoja solar con luz dorada"),
    ("escena_c4_e2.jpg", "Capítulo 4 - Escena 2: Héroe emergiendo con la katana rubí perfecta"),
    ("escena_c4_e3.jpg", "Capítulo 4 - Escena 3: El Líder Supremo esperando con serenidad"),
    ("escena_c5_e1.jpg", "Capítulo 5 - Escena 1: El Rey Demonio entrando al santuario"),
    ("escena_c5_e2.jpg", "Capítulo 5 - Escena 2: Gran explosión destruyendo la sede"),
    ("escena_c5_e3.jpg", "Capítulo 5 - Escena 3: Descenso al Castillo Infinito"),
    ("escena_climax.jpg", "Clímax del Volumen 6 - La explosión destruyendo el santuario")
]

print("Copiando imágenes del Volumen 6 al directorio de artefactos...")
for filename, desc in images:
    src_file = src_dir / filename
    dest_file = artifact_dir / f"vol6_{filename}"
    if src_file.exists():
        shutil.copy2(src_file, dest_file)
        print(f"  [OK] {filename} -> vol6_{filename}")

# Generate Markdown Artifact content
md_path = artifact_dir / "galeria_volumen_6.md"

md_content = """# 🎨 Galería Completa de Ilustraciones - Oni no Ketsuryū Volumen 6

A continuación podés revisar **las 20 ilustraciones HD una por una** del **Volumen 6 (Las Catacumbas del Olvido)**. Podés recorrer el carrusel interactivo o ver el listado detallado más abajo.

---

## 🎠 Carrusel de Inspección Imagen por Imagen

````carousel
"""

carousel_slides = []
for filename, desc in images:
    slide = f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol6_{filename})\n\n**{desc}**"
    carousel_slides.append(slide)

md_content += "\n<!-- slide -->\n".join(carousel_slides)
md_content += "\n````\n\n---\n\n## 🖼️ Listado Detallado Una por Una\n\n"

for filename, desc in images:
    md_content += f"### 📌 {desc}\n\n"
    md_content += f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol6_{filename})\n\n"
    md_content += f"*Archivo local:* [`{filename}`](file:///C:/Proyectos/mis-libros-editorial/libros/oni-no-ketsuryu-volumen-6/{filename})\n\n---\n\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print("¡Artefacto galeria_volumen_6.md creado con éxito!")
