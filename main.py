from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, projects, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    description="API de gestión de tareas con notificaciones asíncronas",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)