@echo off
cd /d "%~dp0"
py diagnostico_servidor.py
if errorlevel 1 python diagnostico_servidor.py
