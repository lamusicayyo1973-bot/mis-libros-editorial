Set w = CreateObject("WScript.Shell")
Set s = w.CreateShortcut("Z:\OneDrive\Desktop\MIS PROYECTOS\Panel Editorial Noguera.lnk")
s.TargetPath = "C:\Proyectos\mis-libros-editorial\Panel_Editorial.bat"
s.WorkingDirectory = "C:\Proyectos\mis-libros-editorial"
s.IconLocation = "C:\Proyectos\mis-libros-editorial\assets\panel_editorial.ico, 0"
s.Description = "Panel de Publicacion Editorial Noguera - 5 Plataformas"
s.Save()
WScript.Echo "Acceso directo actualizado con icono personalizado."
