@echo off
chcp 65001 > nul
title PANEL DE CONTROL DE LOKI (PUBLICACIÓN AUTOMÁTICA DE LIBROS)
cls
echo ================================================================================
echo  🤖 ABRIR PANEL INTERACTIVO DE LOKI
echo ================================================================================
echo  Plataformas: Payhip | Tiendanube | Gumroad | Hotmart | Web Oficial
echo ================================================================================
echo.

powershell -Command "Start-Process 'http://localhost:5000'; Start-Sleep -s 1; (New-Object -ComObject WScript.Shell).AppActivate('Chrome')"

python "C:\Proyectos\mis-libros-editorial\scripts\loki_panel_interactivo.py"

pause
