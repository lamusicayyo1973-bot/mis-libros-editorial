import subprocess
from pathlib import Path

vbs_code = """
Set w = CreateObject("WScript.Shell")
Set s = w.CreateShortcut("Z:\\OneDrive\\Desktop\\MIS PROYECTOS\\Publicar_Libros_Editorial.lnk")
s.TargetPath = "C:\\Proyectos\\mis-libros-editorial\\abrir_panel_de_loki.bat"
s.WorkingDirectory = "C:\\Proyectos\\mis-libros-editorial"
s.Save()
"""

vbs_path = Path("create_shortcut.vbs")
vbs_path.write_text(vbs_code, encoding="utf-8")
subprocess.run(["cscript", "//nologo", "create_shortcut.vbs"])
vbs_path.unlink(missing_ok=True)
print("Shortcut Publicar_Libros_Editorial.lnk created successfully!")
