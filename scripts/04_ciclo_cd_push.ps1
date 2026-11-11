# Micropráctica 11.3 / 11.4 / 11.5 / 11.6 - Ciclo CD: commit + push dispara el auto-deploy en Render
# Uso:  .\scripts\04_ciclo_cd_push.ps1 -Mensaje "feat: agrega endpoint de version 1.2.0"
param(
    [Parameter(Mandatory = $true)][string]$Mensaje
)

git status
git add .
git commit -m $Mensaje
git push origin main
Write-Host "`nPush enviado. Abre Render -> Events / Logs y espera 'Deploy live'." -ForegroundColor Green
