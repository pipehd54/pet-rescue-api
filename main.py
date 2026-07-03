from fastapi import FastAPI
from app.routers import usuarios  # Importaremos nuestro primer router

# Inicializamos la aplicación FastAPI con algo de metadatos para la documentación
app = FastAPI(
    title="API Rescate de Mascotas",
    description="Plataforma comunitaria para reportar mascotas vulnerables",
    version="1.0.0"
)

# Incluimos las rutas (endpoints) de los usuarios
app.include_router(usuarios.router)

# Un endpoint de prueba o "Hola Mundo" en la raíz de la API
@app.get("/")
def ruta_raiz():
    return {
        "mensaje": "¡Bienvenido a la API de Mascotas Vulnerables!",
        "estado": "En línea"
    }