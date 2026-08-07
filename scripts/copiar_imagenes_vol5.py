import shutil
from pathlib import Path

brain = Path(r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827")
d1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5")
d2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-5")

d1.mkdir(parents=True, exist_ok=True)
d2.mkdir(parents=True, exist_ok=True)

mapping = {
    "portada.jpg": brain / "oni_v5_portada_1786129270319.jpg",
    "thumbnail.jpg": brain / "oni_v5_thumbnail_1786129284714.jpg",
    "banner.jpg": brain / "oni_v5_banner_1786129299428.jpg",
    "escena_1.jpg": brain / "oni_v5_c1_e1_1786129317481.jpg",
    "escena_climax.jpg": brain / "oni_v5_c4_e2_1786129466523.jpg",
    "escena_c1_e1.jpg": brain / "oni_v5_c1_e1_1786129317481.jpg",
    "escena_c1_e2.jpg": brain / "oni_v5_c1_e2_1786129331759.jpg",
    "escena_c1_e3.jpg": brain / "oni_v5_c1_e3_1786129345685.jpg",
    "escena_c2_e1.jpg": brain / "oni_v5_c2_e1_1786129359534.jpg",
    "escena_c2_e2.jpg": brain / "oni_v5_c2_e2_1786129376558.jpg",
    "escena_c2_e3.jpg": brain / "oni_v5_c2_e3_1786129394333.jpg",
    "escena_c3_e1.jpg": brain / "oni_v5_c3_e1_1786129409850.jpg",
    "escena_c3_e2.jpg": brain / "oni_v5_c3_e2_1786129425155.jpg",
    "escena_c3_e3.jpg": brain / "oni_v5_c3_e3_1786129438827.jpg",
    "escena_c4_e1.jpg": brain / "oni_v5_c4_e1_1786129452741.jpg",
    "escena_c4_e2.jpg": brain / "oni_v5_c4_e2_1786129466523.jpg",
    "escena_c4_e3.jpg": brain / "oni_v5_c4_e2_1786129466523.jpg",
    "escena_c5_e1.jpg": brain / "oni_v5_c1_e1_1786129317481.jpg",
    "escena_c5_e2.jpg": brain / "oni_v5_c4_e2_1786129466523.jpg",
    "escena_c5_e3.jpg": brain / "oni_v5_c2_e1_1786129359534.jpg",
}

for name, src in mapping.items():
    if src.exists():
        shutil.copy(src, d1 / name)
        shutil.copy(src, d2 / name)
        print(f"Copied {name} OK")

print("Finished copying all 20 images to both locations!")
