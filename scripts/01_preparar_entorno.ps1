# Micropráctica 11.0 - Crea y activa el venv, instala dependencias y congela requirements.txt
# Ejecutar desde la raíz del proyecto:  .\scripts\01_preparar_entorno.ps1
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

if (-not (Test-Path venv)) { python -m venv venv }
& .\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" python-dotenv pytest httpx

# OJO: en Windows PowerShell 5.1, "pip freeze > requirements.txt" guarda en UTF-16 y Render lo rechaza.
# Por eso se fuerza ASCII:
pip freeze | Set-Content -Encoding ascii requirements.txt

Write-Host "`n--- requirements.txt ---" -ForegroundColor Cyan
Get-Content requirements.txt
Write-Host "`n--- .gitignore ---" -ForegroundColor Cyan
Get-Content .gitignore
