from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import io

from app.database import get_db
from app.models import Tarea, Proyecto, Usuario
from app.schemas import TareaCreate, TareaUpdate, TareaOut
from app.routers.auth import get_current_user
from app.tasks.notifications import enviar_notificacion_tarea

router = APIRouter(prefix="/proyectos", tags=["tareas"])


def verificar_proyecto(proyecto_id: int, current_user: Usuario, db: Session):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id, Proyecto.owner_id == current_user.id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


@router.post("/{proyecto_id}/tareas", response_model=TareaOut, status_code=201)
def crear_tarea(proyecto_id: int, tarea: TareaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    verificar_proyecto(proyecto_id, current_user, db)
    nueva = Tarea(**tarea.model_dump(), proyecto_id=proyecto_id)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    if nueva.fecha_limite:
        enviar_notificacion_tarea.delay(current_user.email, nueva.titulo, str(nueva.fecha_limite))
    return nueva


@router.get("/{proyecto_id}/tareas", response_model=list[TareaOut])
def listar_tareas(proyecto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    verificar_proyecto(proyecto_id, current_user, db)
    return db.query(Tarea).filter(Tarea.proyecto_id == proyecto_id).all()


@router.get("/{proyecto_id}/tareas/{tarea_id}", response_model=TareaOut)
def obtener_tarea(proyecto_id: int, tarea_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    verificar_proyecto(proyecto_id, current_user, db)
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id, Tarea.proyecto_id == proyecto_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@router.put("/{proyecto_id}/tareas/{tarea_id}", response_model=TareaOut)
def actualizar_tarea(proyecto_id: int, tarea_id: int, datos: TareaUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    verificar_proyecto(proyecto_id, current_user, db)
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id, Tarea.proyecto_id == proyecto_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(tarea, campo, valor)
    db.commit()
    db.refresh(tarea)
    return tarea


@router.delete("/{proyecto_id}/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(proyecto_id: int, tarea_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    verificar_proyecto(proyecto_id, current_user, db)
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id, Tarea.proyecto_id == proyecto_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()


@router.get("/{proyecto_id}/tareas/export/csv")
def exportar_csv(proyecto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    verificar_proyecto(proyecto_id, current_user, db)
    tareas = db.query(Tarea).filter(Tarea.proyecto_id == proyecto_id).all()
    data = [{"id": t.id, "titulo": t.titulo, "descripcion": t.descripcion, "status": t.status, "fecha_limite": t.fecha_limite, "created_at": t.created_at} for t in tareas]
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=tareas_{proyecto_id}.csv"})