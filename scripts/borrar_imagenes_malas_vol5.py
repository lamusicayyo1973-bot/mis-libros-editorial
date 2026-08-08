import os
from pathlib import Path

vol5 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5")
also_vol5 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-5")

bad_images = [
    "escena_c1_e1.jpg",
    "escena_c1_e2.jpg",
    "escena_c1_e3.jpg",
    "escena_c3_e3.jpg",
    "escena_c4_e1.jpg",
    "escena_c5_e1.jpg",
    "escena_c5_e2.jpg",
    "escena_climax.jpg",
]

for img in bad_images:
    for folder in [vol5, also_vol5]:
        p = folder / img
        if p.exists():
            p.unlink()
            print(f"Deleted: {p}")
        else:
            print(f"Not found: {p}")

print("Done cleaning bad images.")
