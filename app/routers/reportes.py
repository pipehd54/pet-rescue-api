from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, database, models

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"],
    responses={404: {"description": "Reporte no encontrado"}},
)

@router.post("/", response_model=schemas.ReporteResponse, status_code=status.HTTP_201_CREATED)
def crear_reporte(reporte: schemas.ReporteCreate, db: Session = Depends(database.get_db)):
    '''
    Registra un nuevo reporte de mascota vulnerable.
    Nota: Por simplicidad, el usuario_id se envía en el body. 
    En una fase posterior, esto se extraerá del token de autenticación (JWT).
    '''
    # Validación opcional: verificar que el usuario exista antes de crear el reporte
    usuario_existe = db.query(models.Usuario).filter(models.Usuario.id == reporte.usuario_id).first()
    if not usuario_existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario especificado no existe."
        )
    
    return crud.create_reporte(db=db, reporte=reporte, usuario_id=reporte.usuario_id)

@router.get("/", response_model=list[schemas.ReporteResponse])
def listar_reportes(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    '''
    Obtiene una lista paginada de reportes.
    - skip: Numero de registros a omitir (para paginacion).
    - limit: Numero maximo de registros a devolver (evita sobrecargar la memoria).
    '''
    reportes = crud.get_reportes(db, skip=skip, limit=limit)
    return reportes

@router.get("/{reporte_id}", response_model=schemas.ReporteResponse)
def obtener_reporte(rpte_id: int, db: Session = Depends(database.get_db)):
    ''' Obtiene los detalles de un reporte específico, incluyendo sus seguimientos. '''
    db_reporte = crud.get_reporte(db, reporte_id=rpte_id)
    if db_reporte is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El reporte solicitado no existe."
        )
    return db_reporte