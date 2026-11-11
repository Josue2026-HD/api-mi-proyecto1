# Micropráctica 11.0 / 11.2 - Primer push a GitHub (main)
# Uso:  .\scripts\03_git_primer_push.ps1 -RepoUrl "https://github.com/TU_USUARIO/api-mi-proyecto.git"
param(
    [Parameter(Mandatory = $true)][string]$RepoUrl
)

if (-not (Test-Path .git)) { git init }
git branch -M main

# Verificación de seguridad: .env y venv NO deben aparecer
git status --short
$riesgo = git ls-files | Select-String -Pattern '^(\.env$|venv/)'
if ($riesgo) { Write-Host "STOP: hay archivos sensibles en el índice de Git" -ForegroundColor Red; exit 1 }

git add .
git commit -m "chore: audita dependencias y exclusiones para despliegue"

if (-not (git remote)) { git remote add origin $RepoUrl }
git push -u origin main

git status
Write-Host "`nResultado esperado: 'working tree clean'" -ForegroundColor Green
