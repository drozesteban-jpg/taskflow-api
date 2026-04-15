def test_registro_usuario(client):
    response = client.post("/auth/registro", json={
        "email": "test@ejemplo.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@ejemplo.com"


def test_registro_email_duplicado(client):
    client.post("/auth/registro", json={
        "email": "test@ejemplo.com",
        "password": "password123"
    })
    response = client.post("/auth/registro", json={
        "email": "test@ejemplo.com",
        "password": "otrapassword"
    })
    assert response.status_code == 400


def test_login_exitoso(client):
    client.post("/auth/registro", json={
        "email": "test@ejemplo.com",
        "password": "password123"
    })
    response = client.post("/auth/login", data={
        "username": "test@ejemplo.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_credenciales_incorrectas(client):
    response = client.post("/auth/login", data={
        "username": "noexiste@ejemplo.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def get_token(client):
    client.post("/auth/registro", json={
        "email": "test@ejemplo.com",
        "password": "password123"
    })
    response = client.post("/auth/login", data={
        "username": "test@ejemplo.com",
        "password": "password123"
    })
    return response.json()["access_token"]


def test_crear_proyecto(client):
    token = get_token(client)
    response = client.post("/proyectos/", json={
        "nombre": "Proyecto test",
        "descripcion": "Descripcion test"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["nombre"] == "Proyecto test"


def test_listar_proyectos(client):
    token = get_token(client)
    client.post("/proyectos/", json={
        "nombre": "Proyecto test",
        "descripcion": "Descripcion test"
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/proyectos/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_crear_tarea(client, monkeypatch):
    monkeypatch.setattr("app.tasks.notifications.enviar_notificacion_tarea.delay", lambda *args: None)
    token = get_token(client)
    proyecto = client.post("/proyectos/", json={
        "nombre": "Proyecto test",
        "descripcion": "Test"
    }, headers={"Authorization": f"Bearer {token}"})
    proyecto_id = proyecto.json()["id"]
    response = client.post(f"/proyectos/{proyecto_id}/tareas", json={
        "titulo": "Tarea test",
        "descripcion": "Test",
        "fecha_limite": "2026-05-01T10:00:00"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["titulo"] == "Tarea test"