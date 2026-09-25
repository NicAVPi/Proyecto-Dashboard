@echo off
cd /d "%~dp0"
python validar_datos.py
if errorlevel 1 exit /b 1
python app.py
