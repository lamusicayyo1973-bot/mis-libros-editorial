@echo off
title Iniciar Navegador Editorial en Modo Depuracion (Puerto 9222)
echo =========================================================
echo    INICIANDO NAVEGADOR EDITORIAL - PUERTO 9222
echo =========================================================
echo.
echo Cerrando ventanas previas de Brave...
taskkill /IM brave.exe /F 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [*] Abriendo Payhip y Hotmart en el puerto 9222...
start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222 --user-data-dir="c:\Proyectos\loki\config\brave_debug_profile" "https://payhip.com/dashboard" "https://app.hotmart.com/"

echo.
echo [OK] Navegador listo. Logueate si hace falta y manten esta ventana abierta.
timeout /t 5
