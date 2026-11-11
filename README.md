# API de Tareas – Sesión 11: Despliegue Continuo (CD) en Render

Todos los comandos son para **Windows PowerShell** (VS Code → Terminal → Nueva terminal).

## 0. Descomprimir y abrir el proyecto
```powershell
Expand-Archive -Path "$HOME\Downloads\api-mi-proyecto.zip" -DestinationPath "$HOME\Documents" -Force
cd "$HOME\Documents\api-mi-proyecto"
code .
```

## 1. Micropráctica 11.0 – Entorno virtual, requirements y .gitignore
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force   # permite activar venv en esta sesión
python -m venv venv
venv\Scripts\Activate.ps1                                           # debe aparecer (venv)
pip install -r requirements.txt
pip freeze | Set-Content -Encoding ascii requirements.txt           # (no uses ">" en PowerShell 5.1: guarda UTF-16)
Get-Content .gitignore
```
Atajo: `.\scripts\01_preparar_entorno.ps1`

## 2. Micropráctica 11.1 – Probar local (0.0.0.0 + PORT)
```powershell
python -m pytest -q                 # 8 pruebas deben pasar
python main.py                      # Uvicorn running on http://0.0.0.0:8000
# En otra terminal:
curl.exe http://localhost:8000/health
```
Abre también http://localhost:8000/docs. Para simular el puerto del PaaS: `$env:PORT="9000"; python main.py`.

## 3. Micropráctica 11.0 / 11.2 – GitHub y Render
```powershell
git init
git branch -M main
git remote add origin https://github.com/TU_USUARIO/api-mi-proyecto.git
git status                          # NO debe aparecer venv/ ni .env
git add .
git commit -m "chore: audita dependencias y exclusiones para despliegue"
git push -u origin main
git status                          # working tree clean
```
Atajo: `.\scripts\03_git_primer_push.ps1 -RepoUrl "https://github.com/TU_USUARIO/api-mi-proyecto.git"`

En https://render.com (login con GitHub): **+ New → Web Service → Connect `api-mi-proyecto`**

| Campo | Valor |
|---|---|
| Name | api-estudiantes-iesrfa |
| Region | Ohio (US East) / Frankfurt |
| Branch | main |
| Root Directory | *(vacío)* |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | Free |

Clic en **Create Web Service** → espera **Live** → abre `https://TU-API.onrender.com/docs`.
(`render.yaml` incluido es la versión "como código" de esta configuración.)

## 4. Micropráctica 11.3 – Auto-deploy
`main.py` ya incluye `/version`. Ciclo de CD:
```powershell
git status
git add main.py
git commit -m "feat: agrega endpoint de version 1.2.0"
git push origin main
```
Render → *Events*: "Deploy started for commit…" → abre `https://TU-API.onrender.com/version`.

## 5. Micropráctica 11.4 – Variables de entorno
`.env` es local (ignorado por Git) y `.env.example` es la plantilla pública.
```powershell
git add main.py .env.example requirements.txt
git commit -m "feat: variables de entorno con python-dotenv"
git push origin main
git ls-files | Select-String "^\.env$"      # no debe devolver nada
```
Render → servicio → **Environment → Add Environment Variable**:
`API_SECRET_KEY = clave_produccion_render_xyz_987` · `MODO_DEBUG = False` → **Save Changes** (redeploy automático) → `/config-check`.

## 6. Micropráctica 11.5 – Logs
Render → **Logs**. Luego, desde PowerShell:
```powershell
.\scripts\05_probar_nube.ps1 -Url "https://TU-API.onrender.com"
```
Verás en los Runtime Logs: `GET /tareas 200`, `GET /tareas/9999 404`, `GET /ruta-inexistente 404`.

Para provocar el **error 500 de la guía** (ZeroDivisionError + Traceback): en Render → Environment agrega `SIMULAR_ERROR = True`, guarda y abre `/simular-error`. Lee el Traceback en Logs. Para "corregirlo" (paso 9), cambia el valor a `False` (o elimínala): el endpoint pasa a responder 400 controlado y el log se normaliza.

## 7. Micropráctica 11.6 – CORS y cliente web
CORS ya está en `main.py`. Edita `API_URL` en `cliente_web.html` con tu URL de Render y ábrelo:
```powershell
Start-Process .\cliente_web.html
```

## Estructura
```
api-mi-proyecto/
├── main.py                 # API completa
├── test_main.py            # pruebas pytest
├── requirements.txt
├── .gitignore  .env  .env.example
├── render.yaml             # blueprint opcional
├── cliente_web.html        # frontend fetch()
├── RESPUESTAS_SESION_11.md # solucionario
└── scripts/                # 01..05 *.ps1
```
> ⚠️ `.env` va en el ZIP solo por ser material didáctico con claves de práctica; **nunca** lo subas a GitHub.
