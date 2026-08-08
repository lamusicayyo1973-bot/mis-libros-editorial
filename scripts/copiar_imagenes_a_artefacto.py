# -*- coding: utf-8 -*-
import sys
import io
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5")
artifact_dir = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827")

images = [
    ("portada.jpg", "Portada Principal - Samurai con katana ardiendo y cielo rojo"),
    ("thumbnail.jpg", "Miniatura Cuadrada - Aldea de herreros con termas y sakura"),
    ("banner.jpg", "Banner Horizontal - Entrenamiento en bosque de bambú"),
    ("escena_1.jpg", "Escena 1 - Viaje a la aldea oculta con los ojos vendados"),
    ("escena_c1_e1.jpg", "Capítulo 1 - Escena 1: Llegada a la aldea con máscaras Hyottoko"),
    ("escena_c1_e2.jpg", "Capítulo 1 - Escena 2: El anciano jefe muestra el muñeco de entrenamiento"),
    ("escena_c1_e3.jpg", "Capítulo 1 - Escena 3: Katana mítica revelada en el dojo"),
    ("escena_c2_e1.jpg", "Capítulo 2 - Escena 1: Invasión de demonios superiores con cielo de sangre"),
    ("escena_c2_e2.jpg", "Capítulo 2 - Escena 2: El Maestro Celestial de la Niebla desatando su poder helado"),
    ("escena_c2_e3.jpg", "Capítulo 2 - Escena 3: Ataque de demonios alados en la aldea"),
    ("escena_c3_e1.jpg", "Capítulo 3 - Escena 1: Enfrentamiento contra estatuas de buda heladas"),
    ("escena_c3_e2.jpg", "Capítulo 3 - Escena 2: Dragones de madera gigante emergiendo"),
    ("escena_c3_e3.jpg", "Capítulo 3 - Escena 3: Guerrera saltando con katana flexible rosa"),
    ("escena_c4_e1.jpg", "Capítulo 4 - Escena 1: Herrero arrojando la espada dorada entre las llamas"),
    ("escena_c4_e2.jpg", "Capítulo 4 - Escena 2: Combate combinado con fuego solar y demoníaco"),
    ("escena_c4_e3.jpg", "Capítulo 4 - Escena 3: Dragón de lava y desintegración"),
    ("escena_c5_e1.jpg", "Capítulo 5 - Escena 1: Samurai exhausto al amanecer"),
    ("escena_c5_e2.jpg", "Capítulo 5 - Escena 2: Chica retirando bambú y sonriendo al sol"),
    ("escena_c5_e3.jpg", "Capítulo 5 - Escena 3: El Rey Demonio en el castillo infinito"),
    ("escena_climax.jpg", "Clímax de la Saga - Reencuentro de los hermanos bajo los cerezos")
]

print("Copiando imágenes actualizadas al directorio de artefactos...")
for filename, desc in images:
    src_file = src_dir / filename
    dest_file = artifact_dir / f"vol5_v2_{filename}"
    if src_file.exists():
        shutil.copy2(src_file, dest_file)
        print(f"  [OK] {filename} -> vol5_v2_{filename}")

# Generate Markdown Artifact content
md_path = artifact_dir / "galeria_volumen_5.md"

md_content = """# 🎨 Galería Completa de Ilustraciones - Oni no Ketsuryū Volumen 5 (Actualizada)

A continuación podés revisar **las 20 ilustraciones HD una por una** del **Volumen 5**.

---

## 🎠 Carrusel de Inspección Imagen por Imagen

````carousel
"""

carousel_slides = []
for filename, desc in images:
    slide = f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol5_v2_{filename})\n\n**{desc}**"
    carousel_slides.append(slide)

md_content += "\n<!-- slide -->\n".join(carousel_slides)
md_content += "\n````\n\n---\n\n## 🖼️ Listado Detallado Una por Una\n\n"

for filename, desc in images:
    md_content += f"### 📌 {desc}\n\n"
    md_content += f"![{desc}](file:///C:/Users/nicol/.gemini/antigravity/brain/6adf8ce5-9839-4292-a8a1-57beed4c3827/vol5_v2_{filename})\n\n"
    md_content += f"*Archivo local:* [`{filename}`](file:///C:/Proyectos/mis-libros-editorial/libros/oni-no-ketsuryu-volumen-5/{filename})\n\n---\n\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print("¡Artefacto galeria_volumen_5.md creado con éxito!")
