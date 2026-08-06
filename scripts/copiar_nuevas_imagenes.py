import os
import glob
import shutil

brain_dir = r"C:\Users\nicol\.gemini\antigravity\brain\6adf8ce5-9839-4292-a8a1-57beed4c3827"
libros_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros"

mappings = [
    ("oni_vol2_escena_1_*.jpg", "oni-no-ketsuryu-volumen-2", "escena_1.jpg"),
    ("oni_vol2_escena_climax_*.jpg", "oni-no-ketsuryu-volumen-2", "escena_climax.jpg"),
    ("oni_vol3_escena_1_*.jpg", "oni-no-ketsuryu-volumen-3", "escena_1.jpg"),
    ("oni_vol3_escena_climax_*.jpg", "oni-no-ketsuryu-volumen-3", "escena_climax.jpg"),
    ("oni_vol4_escena_1_*.jpg", "oni-no-ketsuryu-volumen-4", "escena_1.jpg"),
    ("oni_vol4_escena_climax_*.jpg", "oni-no-ketsuryu-volumen-4", "escena_climax.jpg"),
]

for pattern, book, target_name in mappings:
    files = glob.glob(os.path.join(brain_dir, pattern))
    if files:
        latest_file = max(files, key=os.path.getmtime)
        dest_path = os.path.join(libros_dir, book, target_name)
        shutil.copy(latest_file, dest_path)
        print(f"Copied {os.path.basename(latest_file)} -> {dest_path}")
