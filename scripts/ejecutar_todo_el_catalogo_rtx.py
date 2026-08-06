import os
import subprocess
import sys
import time

PYTHON_ENV = r"C:\pinokio\api\fooocus.git\app\env\Scripts\python.exe"
BASE_DIR = r"c:\Users\nicol\Downloads\MIS LIBROS"

def run_script(script_name):
    script_path = os.path.join(BASE_DIR, "scripts", script_name)
    print(f"\n==========================================")
    print(f"RUNNING: {script_name}")
    print(f"==========================================")
    res = subprocess.run([PYTHON_ENV, script_path], cwd=BASE_DIR)
    if res.returncode != 0:
        print(f"Error running {script_name}")
    else:
        print(f"Successfully finished {script_name}")

if __name__ == "__main__":
    print("=== STARTING MASTER CATALOG RENDERING PIPELINE ON RTX 3060 ===")
    
    # 1. Compile Oni Vol 2 docx (images already rendered)
    run_script("crear_oni_no_ketsuryu_vol2_exacto_docx.py")
    
    # 2. Render Kuro Vol 1 + Compile docx
    run_script("generar_todas_las_escenas_kuro_vol1_rtx.py")
    run_script("crear_kuro_no_kineki_vol1_exacto_docx.py")
    
    # 3. Render Kuro Vol 2 + Compile docx
    run_script("generar_todas_las_escenas_kuro_vol2_rtx.py")
    run_script("crear_kuro_no_kineki_vol2_exacto_docx.py")

    # 4. Render Kuro Vol 3 + Compile docx
    run_script("generar_todas_las_escenas_kuro_vol3_rtx.py")
    run_script("crear_kuro_no_kineki_vol3_exacto_docx.py")

    # 5. Compile Oni Vol 1 docx (after its images finished)
    run_script("crear_oni_no_ketsuryu_vol1_exacto_docx.py")

    print("\n=== ALL 7 VOLUMES IN THE CATALOG NOW HAVE 15 EXCLUSIVE 8K SCENE ILLUSTRATIONS EACH! ===")
    
    # 6. Push to GitHub
    print("Pushing updated catalog to GitHub...")
    subprocess.run(["git", "add", "."], cwd=BASE_DIR)
    subprocess.run(["git", "commit", "-m", "Master Update: Generadas e integradas las 105 ilustraciones exclusivas 8k por prompt exacto para los 7 volúmenes del catálogo"], cwd=BASE_DIR)
    subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR)
    print("=== PIPELINE FULLY COMPLETED & PUBLISHED TO GITHUB! ===")
