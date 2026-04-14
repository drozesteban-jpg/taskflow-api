from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class TaskStatus(str, enum.Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completada = "completada"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    proyectos = relationship("Proyecto", back_populates="owner")


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    owner = relationship("Usuario", back_populates="proyectos")
    tareas = relationship("Tarea", back_populates="proyecto")


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pendiente)
    fecha_limite = Column(DateTime, nullable=True)
    notificacion_enviada = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)

    proyecto = relationship("Proyecto", back_populates="tareas")