@echo off
title Carga Automatica a Hotmart - Nicolas Noguera Editorial
color 0A

echo =======================================================
echo PREPARANDO BRAVE CON SESION ACTIVA EN PUERTO 9222...
echo =======================================================

echo 1. Cerrando instancias viejas de Brave...
taskkill /F /IM brave.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo 2. Reiniciando Brave en puerto 9222 con tu perfil...
start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222 https://app.hotmart.com/products
timeout /t 6 /nobreak >nul

echo.
echo =======================================================
echo INICIANDO SUBIDA AUTOMATICA DE LIBROS A HOTMART...
echo =======================================================
echo.

python "C:\Proyectos\mis-libros-editorial\scripts\subir_hotmart_cdp.py"

echo.
echo =======================================================
echo PROCESO REVISADO Y FINALIZADO.
echo Press any key to exit.
echo =======================================================
pause
