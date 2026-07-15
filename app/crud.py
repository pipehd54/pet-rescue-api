from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Configuracion de Bcrypt para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    ''' Convierte una contraseña en texto plano a un hash seguro '''
    return pwd_context.hash(password)

def get_usuario_by_email(db: Session, email: str):
    ''' Busca un usuario por su correo electrónico '''
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuario(db: Session, usuario_id: int) -> models.Usuario | None:
    ''' Busca un usuario por su ID. Devuelve None si no existe. '''
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    ''' Crea un nuevo usuario en la base de datos tras hashear su contraseña '''
    hashed_password = get_password_hash(usuario.password)
    db_usuario = models.Usuario(
        email=usuario.email,
        hashed_password=hashed_password,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario) 
    return db_usuario

def create_reporte(db: Session, reporte: schemas.ReporteCreate, usuario_id: int):
    ''' Crea un nuevo reporte asociandolo al usuario que lo genere '''
    db_reporte = models.Reporte(
        titulo=reporte.titulo,
        descripcion=reporte.descripcion,
        sector=reporte.sector,
        usuario_id=usuario_id,
    )
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte

def get_reporte(db: Session, reporte_id: int) -> models.Reporte | None:
    ''' 
    Obtiene un reporte unico por su ID, incluyendo sus seguimientos
    gracias a la relacion definida en models.py 
    '''
    return db.query(models.Reporte).filter(models.Reporte.id == reporte_id).first()

def get_reportes(db: Session, skip: int = 0, limit: int = 100) -> list[models.Reporte]:
    ''' Obtiene una lista de reportes con paginacion basica para optimizar el rendimiento '''
    return db.query(models.Reporte).offset(skip).limit(limit).all()


def create_seguimiento(
    db: Session, seguimiento: schemas.SeguimientoCreate, usuario_id: int
) -> models.Seguimiento:
    '''
    Crea un nuevo seguimiento (comentario) asociado a un reporte y al usuario autor.
    El reporte_id viaja dentro del schema; el usuario_id se pasa por separado
    para simular la futura extracción desde el token JWT (Fase 2 de autenticación).
    '''
    db_seguimiento = models.Seguimiento(
        comentario=seguimiento.comentario,
        reporte_id=seguimiento.reporte_id,
        usuario_id=usuario_id,
    )
    db.add(db_seguimiento)
    db.commit()
    db.refresh(db_seguimiento)
    return db_seguimiento


def get_seguimientos_by_reporte(
    db: Session, reporte_id: int, skip: int = 0, limit: int = 100
) -> list[models.Seguimiento]:
    ''' Obtiene los seguimientos de un reporte específico, ordenados del más reciente al más antiguo. '''
    return (
        db.query(models.Seguimiento)
        .filter(models.Seguimiento.reporte_id == reporte_id)
        .order_by(models.Seguimiento.fecha.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )