from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

# Configuramos el router. 
# prefix="/usuarios" hace que todos los endpoints aquí empiecen con esa ruta.
# tags=["Usuarios"] agrupa estos endpoints en la documentación automática (Swagger).
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificamos si el correo ya está registrado en la base de datos
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # 2. Creamos el objeto del modelo (Por ahora guardamos la contraseña en texto plano
    nuevo_usuario = models.Usuario(
        email=usuario.email, 
        hashed_password=usuario.password 
    )
    
    # 3. Guardamos en la base de datos
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario) # Refrescamos para obtener el ID generado por PostgreSQL
    
    return nuevo_usuario