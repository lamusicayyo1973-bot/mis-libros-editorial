Set w = CreateObject("WScript.Shell")
Set s = w.CreateShortcut("Z:\OneDrive\Desktop\MIS PROYECTOS\Chrome para Editorial (Abrir Primero).lnk")
s.TargetPath = "C:\Proyectos\mis-libros-editorial\Iniciar_Chrome_Editorial.bat"
s.WorkingDirectory = "C:\Proyectos\mis-libros-editorial"
s.IconLocation = "C:\Program Files\Google\Chrome\Application\chrome.exe, 0"
s.Description = "Abre Chrome con automatizacion activa para Payhip y Hotmart"
s.Save()
WScript.Echo "Acceso directo Chrome Editorial creado."
