# Sesión 11 – Solucionario completo (Despliegue Continuo de APIs)

## Preguntas "Reflexiona" de cada micropráctica

**11.0 – ¿Por qué es un error subir `venv/` a GitHub?**
Porque contiene binarios y rutas específicas de Windows (`.exe`, `.dll`, `Scripts\`) que no funcionan en los contenedores Linux de la nube; además pesa cientos de MB, ensucia el historial y es innecesario: `requirements.txt` ya describe cómo recrear el entorno con `pip install -r`.

**11.1 – ¿Por qué `reload=False` en producción?**
`reload` vigila el sistema de archivos y reinicia el servidor al detectar cambios: consume CPU/RAM extra, abre un proceso adicional que puede reiniciarse en mal momento y solo tiene sentido al desarrollar. En la nube el código cambia únicamente con un nuevo despliegue (nuevo contenedor), por lo que debe ir desactivado para tener un proceso estable y predecible.

**11.2 – ¿Quién gestionó Linux, cortafuegos y SSL? ¿Por qué ahorra costos?**
Lo gestionó el proveedor PaaS (Render): sistema operativo, parches, firewall, balanceador, certificado TLS/HTTPS y reinicios. Esto ahorra costos porque no se contrata ni se dedica personal de sistemas a administrar servidores; el equipo solo se ocupa del código (se paga por uso o es gratis en el plan Free).

**11.3 – Error de sintaxis en `main.py` y push a `main`: ¿qué pasa con el contenedor actual?**
Nada: el contenedor que atiende usuarios sigue funcionando. Render construye y arranca el nuevo contenedor aparte (zero downtime); si el build o el arranque fallan, el despliegue se marca como *Failed* y **no** reemplaza la versión vigente. Solo se cambia el tráfico cuando el nuevo contenedor está sano.

**11.4 – ¿Por qué compartir `.env.example` pero jamás `.env`?**
`.env.example` documenta qué variables necesita el proyecto (sin valores reales), de modo que otro desarrollador sepa configurarlo. `.env` contiene secretos reales; si se publica, bots lo detectan en segundos y pueden secuestrar cuentas, bases de datos o generar cobros. (Principio III de Twelve-Factor.)

**11.5 – ¿Por qué mensaje genérico al cliente y detalle en logs?**
El Traceback revela rutas de archivos, nombres de librerías, versiones y lógica interna que un atacante usaría para explotar el sistema (fuga de información). Al cliente se le da "Internal Server Error"; el detalle completo queda en los logs internos, solo accesibles al equipo.

**11.6 – Reto integrador:** resuelto en `main.py` (CORSMiddleware) y `cliente_web.html` (fetch). En el navegador la política SOP bloquea peticiones entre dominios distintos; CORS hace que la API responda con `Access-Control-Allow-Origin`. En empresa se reemplaza `"*"` por el dominio exacto, por ejemplo con la variable `ORIGENES_PERMITIDOS=https://miportafolio.vercel.app`.

## Autoevaluación (11.C)

| # | Respuesta | Justificación |
|---|-----------|---------------|
| 1 | **c** | El webhook de GitHub dispara el despliegue con el `push` a `main`. |
| 2 | **b** | 127.0.0.1 es loopback: solo acepta tráfico local y rechaza al balanceador. |
| 3 | **FALSO** | `.env` es solo local y va en `.gitignore`; en Render se usa la sección *Environment*. |
| 4 | **c** | `pip install -r requirements.txt` |
| 5 | **b** | Runtime Logs del Dashboard (Traceback). |

## Lista de cotejo (20 pts) – dónde se cumple cada criterio

| N.º | Criterio | Pts | Evidencia en el proyecto |
|-----|----------|-----|--------------------------|
| 1 | Repo limpio (requirements, .gitignore, sin venv) | 3 | `requirements.txt`, `.gitignore`, `scripts/01` y `03` |
| 2 | Uvicorn 0.0.0.0 y `$PORT` | 3 | bloque `__main__` de `main.py` |
| 3 | Web Service en Render (Build/Start) | 3 | `render.yaml` y sección 3 del README |
| 4 | Auto-deploy tras `git push` | 3 | `/version` + `scripts/04_ciclo_cd_push.ps1` |
| 5 | Variables de entorno (dotenv + Dashboard) | 3 | `.env`, `.env.example`, `/config-check` |
| 6 | CORS y cliente web | 3 | `CORSMiddleware`, `cliente_web.html` |
| 7 | Inspección de logs | 2 | `/simular-error`, sección 5 del README |

## Anexo B – Errores frecuentes
| Síntoma | Causa | Solución |
|---|---|---|
| `No module named 'fastapi'` | requirements.txt desactualizado (o guardado en UTF-16 desde PowerShell) | `pip freeze \| Set-Content -Encoding ascii requirements.txt`, add, commit, push |
| `Port scan timeout / Failed to bind` | Puerto fijo o 127.0.0.1 | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| `ModuleNotFoundError: main` | Archivo no se llama main.py o está en subcarpeta | Corregir nombre o *Root Directory* |
| CORS: sin `Access-Control-Allow-Origin` | Falta `CORSMiddleware` | Agregarlo en main.py |
| Cold start ~50 s | Plan Free hiberna a los 15 min | Normal; plan Always-On en producción |
