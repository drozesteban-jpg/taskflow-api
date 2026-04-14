from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Proyecto, Usuario
from app.schemas import ProyectoCreate, ProyectoOut
from app.routers.auth import get_current_user

router = APIRouter(prefix="/proyectos", tags=["proyectos"])


@router.post("/", response_model=ProyectoOut, status_code=201)
def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo = Proyecto(**proyecto.model_dump(), owner_id=current_user.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=list[ProyectoOut])
def listar_proyectos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return db.query(Proyecto).filter(Proyecto.owner_id == current_user.id).all()


@router.get("/{proyecto_id}", response_model=ProyectoOut)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id, Proyecto.owner_id == current_user.id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


@router.delete("/{proyecto_id}", status_code=204)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id, Proyecto.owner_id == current_user.id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db.delete(proyecto)
    db.commit()