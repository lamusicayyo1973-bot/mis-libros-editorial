@echo off
title Panel Editorial - Publicador de Libros Noguera
color 0A
echo.
echo  =====================================================
echo   PANEL EDITORIAL - Nicolas Noguera
echo   Publicador automatico en 5 plataformas
echo  =====================================================
echo.
echo  Iniciando servidor en http://localhost:5100 ...
echo.

REM Abrir navegador en el puerto correcto despues de 2 segundos
start /b cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5100"

REM Configurar variable para que los subprocesos hereden la sesion de escritorio
set PYTHONUNBUFFERED=1
set DISPLAY=

REM Iniciar el servidor (esta ventana queda abierta con logs)
python "C:\Proyectos\mis-libros-editorial\scripts\loki_panel_interactivo.py"

echo.
echo  El servidor se detuvo.
pause
