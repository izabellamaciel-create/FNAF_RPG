@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo        FNAF RPG - A ULTIMA NOITE
echo ==========================================
echo.
echo Iniciando servidor local...

taskkill /FI "WINDOWTITLE eq FNAF_RPG_SERVER" /T /F >nul 2>&1

start "FNAF_RPG_SERVER" /D "%~dp0" python -m http.server 8000

timeout /t 2 /nobreak >nul

start "" "http://127.0.0.1:8000/index.html"

echo.
echo O jogo foi aberto no navegador.
echo NAO feche a janela do servidor enquanto estiver jogando.
echo.
echo Para encerrar o servidor, feche esta janela e a janela FNAF_RPG_SERVER.
echo.
pause
