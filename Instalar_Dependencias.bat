@echo off
echo =======================================================
echo  Instalador de Dependencias para Kindle Notes Converter
echo =======================================================
echo.
echo Este script instalara las librerias de Python necesarias (beautifulsoup4, lxml).
echo Asegurate de tener Python instalado y anadido al PATH.
echo.
pause

pip install -r requirements.txt

echo.
echo =======================================================
echo  Instalacion completada.
echo =======================================================
echo.
pause