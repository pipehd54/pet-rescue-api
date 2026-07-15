from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import List, Optional
from .models import EstadoReporte


# ESQUEMAS PARA USUARIOS
class UsuarioBase(BaseModel):
    email: EmailStr # Valida automáticamente que tenga formato de correo (@ y .com)

class UsuarioCreate(UsuarioBase):
    password: str # El usuario envía su contraseña en texto plano para registrarse

class UsuarioResponse(UsuarioBase):
    id: int
    
    # Esto le dice a Pydantic: "Lee los datos de un modelo de SQLAlchemy, no solo de un diccionario"
    model_config = ConfigDict(from_attributes=True)



# ESQUEMAS PARA SEGUIMIENTOS (Comentarios)
class SeguimientoBase(BaseModel):
    comentario: str

class SeguimientoCreate(SeguimientoBase):
    reporte_id: int # Necesitamos saber a qué reporte le estamos comentando

class SeguimientoResponse(SeguimientoBase):
    id: int
    fecha: datetime
    usuario_id: int
    reporte_id: int

    model_config = ConfigDict(from_attributes=True)



# ESQUEMAS PARA REPORTES
class ReporteBase(BaseModel):
    titulo: str
    descripcion: str
    sector: str

class ReporteCreate(ReporteBase):
    usuario_id: int

class ReporteResponse(ReporteBase):
    id: int
    fecha: datetime
    estado: EstadoReporte
    usuario_id: int
    
    # Opcional: Podemos incluir los seguimientos dentro de la respuesta del reporte
    seguimientos: List[SeguimientoResponse] = []

    model_config = ConfigDict(from_attributes=True)