@echo off
echo ============================================================
echo  PASO 2: Cargando El Algoritmo Personal en las plataformas
echo ============================================================
echo.
echo  Asegurate de haber ejecutado PASO_1 primero y que Chrome
echo  este abierto con las 4 pestañas visibles en pantalla.
echo.
pause

python "C:\Proyectos\mis-libros-editorial\scripts\publicar_el_algoritmo_via_cdp.py"

echo.
echo ============================================================
echo  PROCESO TERMINADO - Fijate en Chrome si se cargaron los datos
echo ============================================================
pause
