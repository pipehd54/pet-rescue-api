from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, database, models

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"], # Agrupa los endpoints en la documentación automática (Swagger).
    responses={404: {"description": "No encontrado"}}
)

@router.post("/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    ''' 
    Registra un nuevo usuario en la plataforma,
    valida que el correo no este registrado y hashea la contraseña
    '''
    # 1. Verificar si el usuario ya existe
    db_user = crud.get_usuario_by_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electronico ya esta registrado"
        )
    
    # 2. Crear el usuario a traves del CRUD
    return crud.create_usuario(db, usuario=usuario)

@router.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    ''' Obtiene la informacion publica de un usuario por su ID '''
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return db_usuario