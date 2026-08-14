# -*- coding: utf-8 -*-
import sys
import io
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-9")
artifact_dir = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827")

images = [
    ("portada.jpg", "Portada Principal - Ren ejecutando la Decimotercera Postura Solar"),
    ("thumbnail.jpg", "Miniatura Cuadrada - El Rey Demonio Kageyama con tentáculos látigo"),
    ("banner.jpg", "Banner Horizontal - Batalla en las ruinas urbanas al amanecer"),
    ("escena_1.jpg", "Escena 1 - Emergencia del Rey Demonio en la plaza de la ciudad"),
    ("escena_c1_e1.jpg", "Capítulo 1 - Escena 1: Guerreros saliendo de los escombros de la ciudad"),
    ("escena_c1_e2.jpg", "Capítulo 1 - Escena 2: Látigos espinados cortando edificios de piedra"),
    ("escena_c1_e3.jpg", "Capítulo 1 - Escena 3: Portador medicinal entregando antídotos en tejados"),
    ("escena_c2_e1.jpg", "Capítulo 2 - Escena 1: La toxina de Sumire haciendo envejecer a Kageyama"),
    ("escena_c2_e2.jpg", "Capítulo 2 - Escena 2: Asalto combinado del Pilar de la Piedra y Viento"),
    ("escena_c2_e3.jpg", "Capítulo 2 - Escena 3: Ren recordando la sabiduría ancestral"),
    ("escena_c3_e1.jpg", "Capítulo 3 - Escena 1: Cadena continua de posturas solares en forma de dragón"),
    ("escena_c3_e2.jpg", "Capítulo 3 - Escena 2: Choque de látigos de materia oscura vs fuego solar"),
    ("escena_c3_e3.jpg", "Capítulo 3 - Escena 3: Reloj gigantesco marcando 15 minutos para el amanecer"),
    ("escena_c4_e1.jpg", "Capítulo 4 - Escena 1: Transformación monstruosa en bebé gigante de carne"),
    ("escena_c4_e2.jpg", "Capítulo 4 - Escena 2: Guerreros reteniendo al demonio gigante con cadenas"),
    ("escena_c4_e3.jpg", "Capítulo 4 - Escena 3: Estocada solar clavando a Kageyama contra el muro"),
    ("escena_c5_e1.jpg", "Capítulo 5 - Escena 1: Los primeros rayos de sol desintegrando la masa demoníaca"),
    ("escena_c5_e2.jpg", "Capítulo 5 - Escena 2: Disolución final de la conciencia del Rey Demonio"),
    ("escena_c5_e3.jpg", "Capítulo 5 - Escena 3: Amanecer pacífico sobre las ruinas victoriosas"),
    ("escena_climax.jpg", "Clímax del Volumen 9 - Desintegración solar definitiva")
]

print("Copiando imágenes del Volumen 9 al directorio de artefactos...")
for filename, desc in images:
    src_file = src_dir / filename
    dest_file = artifact_dir / f"vol9_{filename}"
    if src_file.exists():
        shutil.copy2(src_file, dest_file)
        print(f"  [OK] {filename} -> vol9_{filename}")

# Generate Markdown Artifact content
md_path = artifact_dir / "galeria_volumen_9.md"

md_content = """# 🎨 Galería Completa de Ilustraciones - Oni no Ketsuryū Volumen 9

A continuación podés revisar **las 20 ilustraciones HD una por una** del **Volumen 9 (La Noche de los Noventa Minutos)**. Podés recorrer el carrusel interactivo o ver el listado detallado más abajo.

---

## 🎠 Carrusel de Inspección Imagen por Imagen

````carousel
"""

carousel_slides = []
for filename, desc in images:
    slide = f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol9_{filename})\n\n**{desc}**"
    carousel_slides.append(slide)

md_content += "\n<!-- slide -->\n".join(carousel_slides)
md_content += "\n````\n\n---\n\n## 🖼️ Listado Detallado Una por Una\n\n"

for filename, desc in images:
    md_content += f"### 📌 {desc}\n\n"
    md_content += f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol9_{filename})\n\n"
    md_content += f"*Archivo local:* [`{filename}`](file:///C:/Proyectos/mis-libros-editorial/libros/oni-no-ketsuryu-volumen-9/{filename})\n\n---\n\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print("¡Artefacto galeria_volumen_9.md creado con éxito!")
