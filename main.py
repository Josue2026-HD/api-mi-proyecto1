"""
API REST de Tareas - Sesión 11: Despliegue Continuo (CD) en la nube
IES "República Federal de Alemania" - Chiclayo
Incluye: Health Check, versión, variables de entorno, CORS, logs y endpoint de diagnóstico.
"""
import logging
import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Carga las variables del archivo .env local si existe (en Render se usan las del Dashboard)
load_dotenv()

logger = logging.getLogger("uvicorn.error")

SECRET_KEY = os.getenv("API_SECRET_KEY", "clave_por_defecto_insegura")
MODO_DEBUG = os.getenv("MODO_DEBUG", "False")
MAX_REGISTROS = int(os.getenv("MAX_REGISTROS", "100"))

app = FastAPI(
    title="API de Tareas - Sesión 11 (CD en la nube)",
    description="API RESTful con FastAPI desplegada con Despliegue Continuo en Render.",
    version="1.2.0",
)

# ---------------------------------------------------------------- CORS (Micropráctica 11.6)
# En aprendizaje se permite cualquier origen. En empresas se especifica el dominio exacto.
origins = [o.strip() for o in os.getenv("ORIGENES_PERMITIDOS", "*").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------- Modelos (Sesión 10)
class TareaIn(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    completada: bool = False


class Tarea(TareaIn):
    id: int


tareas_db: List[Tarea] = [
    Tarea(id=1, titulo="Desplegar API en Render", descripcion="Conectar GitHub con Render", completada=False),
    Tarea(id=2, titulo="Configurar variables de entorno", descripcion="Usar .env y Dashboard", completada=False),
]


def _siguiente_id() -> int:
    return max((t.id for t in tareas_db), default=0) + 1


# ---------------------------------------------------------------- CRUD de tareas
@app.get("/", tags=["Sistema"])
def raiz():
    return {"mensaje": "API de Tareas en la nube. Visita /docs para Swagger UI."}


@app.get("/tareas", response_model=List[Tarea], tags=["Tareas"])
def listar_tareas():
    return tareas_db


@app.get("/tareas/{tarea_id}", response_model=Tarea, tags=["Tareas"])
def obtener_tarea(tarea_id: int):
    for t in tareas_db:
        if t.id == tarea_id:
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@app.post("/tareas", response_model=Tarea, status_code=201, tags=["Tareas"])
def crear_tarea(tarea: TareaIn):
    if len(tareas_db) >= MAX_REGISTROS:
        raise HTTPException(status_code=409, detail=f"Límite de {MAX_REGISTROS} registros alcanzado")
    nueva = Tarea(id=_siguiente_id(), **tarea.model_dump())
    tareas_db.append(nueva)
    return nueva


@app.put("/tareas/{tarea_id}", response_model=Tarea, tags=["Tareas"])
def actualizar_tarea(tarea_id: int, datos: TareaIn):
    for i, t in enumerate(tareas_db):
        if t.id == tarea_id:
            tareas_db[i] = Tarea(id=tarea_id, **datos.model_dump())
            return tareas_db[i]
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@app.delete("/tareas/{tarea_id}", status_code=204, tags=["Tareas"])
def eliminar_tarea(tarea_id: int):
    for i, t in enumerate(tareas_db):
        if t.id == tarea_id:
            tareas_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


# ---------------------------------------------------------------- Micropráctica 11.1: Health Check
@app.get("/health", tags=["Sistema"])
def health_check():
    return {
        "status": "online",
        "ambiente": os.getenv("ENVIRONMENT", "desarrollo_local"),
        "servidor": "FastAPI + Uvicorn Cloud",
    }


# ---------------------------------------------------------------- Micropráctica 11.3: Versión
@app.get("/version", tags=["Sistema"])
def consultar_version():
    return {
        "version": "1.2.0",
        "descripcion": "API desplegada mediante Continuous Deployment desde GitHub",
        "docente": "Lic. Ronald J. Villar Gonzales",
        "institucion": "IES República Federal de Alemania - Chiclayo",
    }


# ---------------------------------------------------------------- Micropráctica 11.4: Variables de entorno
@app.get("/config-check", tags=["Seguridad"])
def config_check():
    return {
        "modo_debug": MODO_DEBUG,
        # Buena práctica: nunca reveles el valor completo del secreto en logs o endpoints
        "clave_configurada": SECRET_KEY != "clave_por_defecto_insegura",
        "prefijo_clave": SECRET_KEY[:4] + "****",
    }


# ---------------------------------------------------------------- Micropráctica 11.5: Diagnóstico de logs
@app.get("/simular-error", tags=["Diagnóstico"])
def simular_error():
    """
    Con SIMULAR_ERROR=True provoca la ZeroDivisionError de la guía (error 500 + Traceback en logs).
    Por defecto (versión CORREGIDA, paso 9 de la guía) el error se maneja y se responde 400.
    """
    if os.getenv("SIMULAR_ERROR", "False").lower() == "true":
        resultado = 10 / 0  # División por cero: excepción no controlada
        return {"resultado": resultado}
    try:
        resultado = 10 / 0
    except ZeroDivisionError:
        logger.warning("Error controlado en /simular-error: división por cero")
        raise HTTPException(status_code=400, detail="Operación inválida: división por cero")
    return {"resultado": resultado}


# ---------------------------------------------------------------- Micropráctica 11.1: Arranque productivo
if __name__ == "__main__":
    import uvicorn

    # Lee el puerto inyectado por el PaaS; si no existe, usa 8000 por defecto
    puerto = int(os.environ.get("PORT", 8000))
    # Escucha obligatoria en 0.0.0.0 para entornos en la nube
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)
