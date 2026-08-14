@echo off
echo Abriendo Edge para Hotmart...
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9223 https://app.hotmart.com
echo.
echo Si no se abrio, probando otra ruta...
start "" "C:\Program Files\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9223 https://app.hotmart.com
echo.
echo Edge deberia haberse abierto con Hotmart.
echo Logueate y despues avisame en el chat.
pause
