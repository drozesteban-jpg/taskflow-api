# TaskFlow API

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.4-37814A?style=flat)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

API REST de gestión de tareas con notificaciones asíncronas por email. Permite crear proyectos, asignar tareas con fecha límite y recibir recordatorios automáticos via Celery + Redis.

🚀 **Demo en producción:** [https://taskflow-api-production-1236.up.railway.app/docs](https://taskflow-api-production-1236.up.railway.app/docs)

---

## Funcionalidades

- Registro y login de usuarios con JWT
- CRUD completo de proyectos y tareas
- Notificaciones asíncronas por email al crear tareas con fecha límite
- Export de tareas a CSV
- Filtro de tareas por estado

---

## Tecnologías

- **Python 3.11**
- **FastAPI** — framework web
- **PostgreSQL** — base de datos
- **SQLAlchemy 2.0** — ORM
- **Celery + Redis** — procesamiento asíncrono de tareas
- **Resend** — envío de emails via API
- **Pydantic** — validación de datos
- **python-jose** — JWT
- **passlib + bcrypt** — hash de contraseñas
- **pandas** — export a CSV
- **Docker** — contenedores

---

## Arquitectura

Cliente → FastAPI → PostgreSQL
↓
Redis (broker)
↓
Celery Worker → Resend API → Email

---

## Instalación con Docker

```bash
git clone https://github.com/drozesteban-jpg/taskflow-api.git
cd taskflow-api
```

Creá un archivo `.env` en la raíz:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/taskflow
SECRET_KEY=tu_clave_secreta
REDIS_URL=redis://redis:6379/0
RESEND_API_KEY=re_tu_api_key
```

Levantá los contenedores:

```bash
docker compose up --build
```

Accedé a la documentación en: http://localhost:8000/docs

---

## Endpoints

### Autenticación

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /auth/registro | Registrar usuario | No |
| POST | /auth/login | Obtener token JWT | No |

### Proyectos

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /proyectos/ | Crear proyecto | Sí |
| GET | /proyectos/ | Listar proyectos | Sí |
| GET | /proyectos/{id} | Obtener proyecto | Sí |
| DELETE | /proyectos/{id} | Eliminar proyecto | Sí |

### Tareas

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /proyectos/{id}/tareas | Crear tarea | Sí |
| GET | /proyectos/{id}/tareas | Listar tareas | Sí |
| GET | /proyectos/{id}/tareas/{id} | Obtener tarea | Sí |
| PUT | /proyectos/{id}/tareas/{id} | Actualizar tarea | Sí |
| DELETE | /proyectos/{id}/tareas/{id} | Eliminar tarea | Sí |
| GET | /proyectos/{id}/tareas/export/csv | Exportar a CSV | Sí |

---

## Ejemplo de uso

**1. Registrar usuario:**

```bash
curl -X POST http://localhost:8000/auth/registro \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "mi_clave"}'
```

**2. Crear una tarea con fecha límite:**

```bash
curl -X POST http://localhost:8000/proyectos/1/tareas \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Revisar PR", "fecha_limite": "2026-05-01T10:00:00"}'
```

Al crear la tarea, Celery envía automáticamente un email de recordatorio.

---

## Tests

```bash
pytest tests/
```

---

## Estructura del proyecto

taskflow-api/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── README.md
├── app/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── projects.py
│   │   └── tasks.py
│   └── tasks/
│       ├── celery_app.py
│       └── notifications.py
└── tests/
├── conftest.py
└── test_tasks.py

---

## Autor

**Esteban Droz** — [@drozesteban-jpg](https://github.com/drozesteban-jpg)

Proyecto desarrollado para consolidar conocimientos en Python backend, arquitecturas asíncronas y APIs REST.