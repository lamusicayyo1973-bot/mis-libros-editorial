@echo off
chcp 65001 > nul
title LOKI AUTO-PUBLISHER MULTIPLATAFORMA (5 PLATAFORMAS)
cls
echo ================================================================================
echo  🤖 LOKI AUTO-PUBLISHER: CARGA AUTOMÁTICA POR CARPETA (5 PLATAFORMAS INCLUIDAS)
echo ================================================================================
echo  1. Payhip
echo  2. Tiendanube Argentina
echo  3. Gumroad
echo  4. Hotmart
echo  5. Amazon KDP
echo ================================================================================
echo.

if "%~1"=="" (
    set /p CARPETA_PATH="👉 Arrastrá la carpeta del libro acá o pegá su dirección: "
) else (
    set CARPETA_PATH="%~1"
)

python "c:\Users\nicol\Downloads\MIS LIBROS\scripts\loki_auto_publisher.py" %CARPETA_PATH%

pause
