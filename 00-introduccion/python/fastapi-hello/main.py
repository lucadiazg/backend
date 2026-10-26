"""
Módulo principal de la API Hola Mundo con FastAPI.

FastAPI es un framework web moderno y rápido (de alto rendimiento)
para construir APIs con Python 3.8+ basado en type hints estándar.

Características clave que se demuestran aquí:
  - Type hints como ciudadanos de primera clase
  - Documentación automática e interactiva (OpenAPI / Swagger)
  - Validación automática de parámetros con Pydantic
  - Async nativo
  - Inyección de dependencias

Para ejecutar:
    $ uvicorn main:app --reload --port 8000

Documentación interactiva (una vez ejecutando):
    - Swagger UI: http://localhost:8000/docs
    - ReDoc:     http://localhost:8000/redoc
"""
import logging
from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Instancia de la aplicación
# ---------------------------------------------------------------------------
# FastAPI() recibe parámetros de configuración que se reflejan en la
# documentación automática. El tipo `app` se infiere como `FastAPI`.
app = FastAPI(
    title="Hola Mundo - FastAPI",
    description="API de ejemplo para el curso de Desarrollo Web - Backend",
    version="0.1.0",
    # Los docs se sirven en /docs por defecto, se puede personalizar:
    # docs_url="/api/docs",
)

class SaludoRequest(BaseModel):
    nombre: str
    edad: int

# ---------------------------------------------------------------------------
# Endpoint raíz
# ---------------------------------------------------------------------------
# El decorador `@app.get("/")` asocia esta función a una petición GET en "/".
# FastAPI infiere automáticamente:
#   - El método HTTP del decorador
#   - El tipo de retorno (dict → JSON)
#   - El schema OpenAPI a partir del type hint de retorno
@app.get("/")
def read_root(name: str | None = None):
    logger.info("Se consultó el endpoint raíz")

    if name:
        return {"message": f"¡Hola, {name} desde FastAPI!"}

    return {"message": "¡Hola, mundo desde FastAPI!"}

@app.get("/version")
def version():
    return {"version": "0.1.0"}

# ---------------------------------------------------------------------------
# Endpoint de salud
# ---------------------------------------------------------------------------
# Los endpoints de health check son un estándar en APIs productivas.
# Permiten a balanceadores de carga, orquestadores y monitores
# verificar que la aplicación está viva y respondiendo.
@app.get("/health")
def health_check():
    """
    Health check de la API.
    Retorna el estado del servicio.

    Es una buena práctica separar los endpoints de monitoreo
    de los endpoints de negocio.
    """
    return {"status": "ok", "service": "fastapi-hello"}


@app.post("/saludos")
def crear_saludo(datos: SaludoRequest):
    return {
        "message": f"¡Hola, {datos.nombre}! Tenés {datos.edad} años."
    }