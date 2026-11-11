# Micropráctica 11.2 - 11.5 - Prueba los endpoints de la API desplegada
# Uso:  .\scripts\05_probar_nube.ps1 -Url "https://api-estudiantes-iesrfa.onrender.com"
param(
    [Parameter(Mandatory = $true)][string]$Url
)

function Probar($ruta) {
    Write-Host "`nGET $ruta" -ForegroundColor Cyan
    try {
        $r = Invoke-WebRequest -Uri "$Url$ruta" -UseBasicParsing -TimeoutSec 90
        Write-Host "HTTP $($r.StatusCode)" -ForegroundColor Green
        $r.Content
    } catch {
        $code = [int]$_.Exception.Response.StatusCode
        Write-Host "HTTP $code" -ForegroundColor Yellow
    }
}

Write-Host "(La primera petición puede tardar 40-60 s por el cold start del plan Free)"
Probar "/health"
Probar "/version"
Probar "/config-check"
Probar "/tareas"            # 200 OK
Probar "/tareas/9999"       # 404 controlado
Probar "/ruta-inexistente"  # 404
Probar "/simular-error"     # 400 (corregido) o 500 si SIMULAR_ERROR=True en Render

Write-Host "`nAhora revisa Render -> Logs para ver el tráfico INFO y el Traceback." -ForegroundColor Green
