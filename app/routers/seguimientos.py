from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, database

router = APIRouter(
    prefix="/seguimientos",
    tags=["Seguimientos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=schemas.SeguimientoResponse, status_code=status.HTTP_201_CREATED)
def crear_seguimiento(
    seguimiento: schemas.SeguimientoCreate,
    usuario_id: int,
    db: Session = Depends(database.get_db),
):
    '''
    Registra un nuevo seguimiento (comentario) sobre un reporte existente.

    Nota: `usuario_id` se recibe como query param por simplicidad.
    En la Fase 2 (JWT) se extraerá automáticamente del token de autenticación
    en lugar de que el cliente lo declare explícitamente.
    '''
    # 1. Verificar que el reporte al que se comenta realmente existe
    db_reporte = crud.get_reporte(db, reporte_id=seguimiento.reporte_id)
    if db_reporte is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El reporte especificado no existe.",
        )

    # 2. Verificar que el usuario autor existe
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario especificado no existe.",
        )

    return crud.create_seguimiento(db, seguimiento=seguimiento, usuario_id=usuario_id)


@router.get("/reporte/{reporte_id}", response_model=list[schemas.SeguimientoResponse])
def listar_seguimientos_por_reporte(
    reporte_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(database.get_db),
):
    '''
    Obtiene los seguimientos (comentarios) de un reporte específico,
    ordenados del más reciente al más antiguo, con paginación.
    '''
    # Verificamos que el reporte exista antes de listar sus seguimientos,
    # para distinguir entre "reporte sin comentarios" (200, lista vacía)
    # y "reporte inexistente" (404).
    db_reporte = crud.get_reporte(db, reporte_id=reporte_id)
    if db_reporte is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El reporte especificado no existe.",
        )

    return crud.get_seguimientos_by_reporte(db, reporte_id=reporte_id, skip=skip, limit=limit)
