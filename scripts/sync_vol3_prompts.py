import os
import glob
import shutil

brain_dir = r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827"
vol3_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-3"

mappings = [
    ("oni_vol3_portada_*.jpg", "portada.jpg"),
    ("oni_vol3_thumbnail_*.jpg", "thumbnail.jpg"),
    ("oni_vol3_banner_*.jpg", "banner.jpg"),
    ("oni_v3_c1_e1_*.jpg", "escena_c1_e1.jpg"),
    ("oni_v3_c1_e2_*.jpg", "escena_c1_e2.jpg"),
    ("oni_v3_c1_e3_*.jpg", "escena_c1_e3.jpg"),
    ("oni_v3_c2_e1_*.jpg", "escena_c2_e1.jpg")
]

for pattern, dest_name in mappings:
    files = glob.glob(os.path.join(brain_dir, pattern))
    if files:
        latest = max(files, key=os.path.getmtime)
        shutil.copy(latest, os.path.join(vol3_dir, dest_name))
        print(f"Copied {os.path.basename(latest)} -> {dest_name}")
