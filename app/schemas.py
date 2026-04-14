from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models import TaskStatus


# ── Auth ──────────────────────────────────────────────
class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str

class UsuarioOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


# ── Proyectos ─────────────────────────────────────────
class ProyectoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class ProyectoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Tareas ────────────────────────────────────────────
class TareaCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    fecha_limite: Optional[datetime] = None

class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    status: Optional[TaskStatus] = None
    fecha_limite: Optional[datetime] = None

class TareaOut(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    status: TaskStatus
    fecha_limite: Optional[datetime]
    created_at: datetime
    proyecto_id: int

    class Config:
        from_attributes = True