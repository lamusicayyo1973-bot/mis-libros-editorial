# -*- coding: utf-8 -*-
import sys
import io
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-10")
artifact_dir = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827")

images = [
    ("portada.jpg", "Portada Principal - Ren y Miyuki al amanecer bajo cerezos en flor"),
    ("thumbnail.jpg", "Miniatura Cuadrada - Curación de Ren con luz solar cálida"),
    ("banner.jpg", "Banner Horizontal - Aldea de montaña pacífica al amanecer"),
    ("escena_1.jpg", "Escena 1 - Silencio del alba tras la batalla final"),
    ("escena_c1_e1.jpg", "Capítulo 1 - Escena 1: Miyuki curando las heridas de su hermano"),
    ("escena_c1_e2.jpg", "Capítulo 1 - Escena 2: Ceremonia rindiendo katanas en el altar"),
    ("escena_c1_e3.jpg", "Capítulo 1 - Escena 3: Tienda médica de paz al amanecer"),
    ("escena_c2_e1.jpg", "Capítulo 2 - Escena 1: Abrazo emotivo de los camaradas victoriosos"),
    ("escena_c2_e2.jpg", "Capítulo 2 - Escena 2: Disolución de la Hermandad del Sol"),
    ("escena_c2_e3.jpg", "Capítulo 2 - Escena 3: Regreso al hogar en el monte Kurodake"),
    ("escena_c3_e1.jpg", "Capítulo 3 - Escena 1: Guardando la katana solar en el relicario"),
    ("escena_c3_e2.jpg", "Capítulo 3 - Escena 2: Jardín de glicinas y rosas en paz"),
    ("escena_c3_e3.jpg", "Capítulo 3 - Escena 3: La forja familiar convertida en herrería de paz"),
    ("escena_c4_e1.jpg", "Capítulo 4 - Escena 1: Contando la leyenda del Sol a los niños"),
    ("escena_c4_e2.jpg", "Capítulo 4 - Escena 2: Linternas de papel flotando hacia el cielo nocturno"),
    ("escena_c4_e3.jpg", "Capítulo 4 - Escena 3: El sol naciente sobre las montañas ancestrales"),
    ("escena_c5_e1.jpg", "Capítulo 5 - Escena 1: Transición al Tokio moderno al amanecer"),
    ("escena_c5_e2.jpg", "Capítulo 5 - Escena 2: Reencarnaciones disfrutando de la vida pacífica"),
    ("escena_c5_e3.jpg", "Capítulo 5 - Escena 3: Renacer bajo los cerezos en el Tokio moderno"),
    ("escena_climax.jpg", "Clímax de la Saga - Cierre definitivo bajo los cerezos de Tokio")
]

print("Copiando imágenes actualizadas del Volumen 10 al directorio de artefactos...")
for filename, desc in images:
    src_file = src_dir / filename
    dest_file = artifact_dir / f"vol10_v4_{filename}"
    if src_file.exists():
        shutil.copy2(src_file, dest_file)
        print(f"  [OK] {filename} -> vol10_v4_{filename}")

# Generate Markdown Artifact content
md_path = artifact_dir / "galeria_volumen_10.md"

md_content = """# 🎨 Galería Completa de Ilustraciones - Oni no Ketsuryū Volumen 10 (Personajes Anime Adultos Definitivos)

A continuación podés revisar **las 20 ilustraciones HD una por una** del **Volumen 10 (El Amanecer del Acero Santo - Gran Final)**. Podés recorrer el carrusel interactivo o ver el listado detallado más abajo.

---

## 🎠 Carrusel de Inspección Imagen por Imagen

````carousel
"""

carousel_slides = []
for filename, desc in images:
    slide = f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol10_v4_{filename})\n\n**{desc}**"
    carousel_slides.append(slide)

md_content += "\n<!-- slide -->\n".join(carousel_slides)
md_content += "\n````\n\n---\n\n## 🖼️ Listado Detallado Una por Una\n\n"

for filename, desc in images:
    md_content += f"### 📌 {desc}\n\n"
    md_content += f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol10_v4_{filename})\n\n"
    md_content += f"*Archivo local:* [`{filename}`](file:///C:/Proyectos/mis-libros-editorial/libros/oni-no-ketsuryu-volumen-10/{filename})\n\n---\n\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print("¡Artefacto galeria_volumen_10.md actualizado con éxito!")
