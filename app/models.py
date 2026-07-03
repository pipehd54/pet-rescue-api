from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base

# Estados válidos para el ciclo de vida de un reporte.
class EstadoReporte(str, enum.Enum):
    activo = "Activo"
    en_proceso = "En Proceso"
    resuelto = "Resuelto"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    reportes = relationship("Reporte", back_populates="creador")
    seguimientos = relationship("Seguimiento", back_populates="autor")

class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    sector = Column(String, nullable=False)
    estado = Column(Enum(EstadoReporte), default=EstadoReporte.activo)

    # Relación con el usuario que crea el reporte.
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    creador = relationship("Usuario", back_populates="reportes")
    seguimientos = relationship("Seguimiento", back_populates="reporte")

class Seguimiento(Base):
    __tablename__ = "seguimientos"

    id = Column(Integer, primary_key=True, index=True)
    comentario = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Vincula cada seguimiento con su reporte y el usuario que lo registró.
    reporte_id = Column(Integer, ForeignKey("reportes.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    reporte = relationship("Reporte", back_populates="seguimientos")
    autor = relationship("Usuario", back_populates="seguimientos")