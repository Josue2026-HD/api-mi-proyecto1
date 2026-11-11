# Micropráctica 11.1 - Prueba local (equivale a Render, pero en tu PC)
# Ejecutar:  .\scripts\02_probar_local.ps1
& .\venv\Scripts\Activate.ps1

Write-Host "Ejecutando pruebas automáticas..." -ForegroundColor Cyan
python -m pytest -q

# Simula el puerto dinámico que inyecta el PaaS
$env:PORT = "8000"
Write-Host "`nIniciando API en http://0.0.0.0:$($env:PORT)  (Ctrl+C para detener)" -ForegroundColor Green
Write-Host "Abre: http://localhost:8000/health  |  /docs  |  /version  |  /config-check"
python main.py
