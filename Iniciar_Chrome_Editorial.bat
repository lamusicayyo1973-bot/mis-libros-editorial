@echo off
title Loki - Abrir Chrome para Automatizacion (una sola vez)
color 0B
echo.
echo  =====================================================
echo   CONFIGURACION UNICA - Chrome con Automatizacion
echo   (Solo necesitas hacer esto una vez por sesion)
echo  =====================================================
echo.
echo  1. Cerrando Chrome actual...
taskkill /F /IM chrome.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo  2. Abriendo Chrome con tu perfil real + puerto de automatizacion...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\Users\nicol\AppData\Local\Google\Chrome\User Data" ^
  --profile-directory="Default" ^
  --start-maximized ^
  --no-first-run ^
  --no-default-browser-check

echo.
echo  3. Chrome abierto con automatizacion activa.
echo     Ya podes volver al Panel Editorial y usar el boton de Payhip/Hotmart.
echo.
echo  NOTA: Mientras uses el Panel, NO cierres esta ventana de Chrome.
echo        Cuando termines de publicar, podes cerrar Chrome normalmente.
echo.
pause
