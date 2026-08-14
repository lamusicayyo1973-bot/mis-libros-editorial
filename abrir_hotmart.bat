@echo off
echo Abriendo Brave para Hotmart...
start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\brave-hotmart-session" https://app.hotmart.com
echo.
echo Se abrio la ventana de Brave con Hotmart.
echo Por favor ingresa tu usuario y clave.
echo Cuando veas el panel de Hotmart, avisa "Listo" en el chat.
pause
