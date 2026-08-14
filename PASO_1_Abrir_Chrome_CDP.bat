@echo off
echo ============================================================
echo  Lanzando Chrome con TU perfil real + puerto CDP 9222
echo  (Todos tus logins de Chrome se van a mantener activos)
echo ============================================================

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --profile-directory="Default" ^
  --user-data-dir="C:\Users\nicol\AppData\Local\Google\Chrome\User Data" ^
  --start-maximized ^
  "https://nicolasnogueraeditorial.mitiendanube.com/admin/products/new" ^
  "https://payhip.com/product/add/digital" ^
  "https://gumroad.com/products/new" ^
  "https://app.hotmart.com/tools/products/create"

echo.
echo Chrome abierto. Espera 10 segundos y ejecuta PASO_2.
echo.
pause
