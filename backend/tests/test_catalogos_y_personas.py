def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


# ---------- Catálogos ----------
def test_listar_estados(client):
    r = client.get("/estados")
    assert r.status_code == 200
    nombres = [e["nombre"] for e in r.json()]
    assert nombres == ["Abierto", "En progreso", "Resuelto", "Cerrado"]


def test_listar_urgencias(client):
    r = client.get("/urgencias")
    assert r.status_code == 200
    riesgos = {u["nombre"]: u["riesgo"] for u in r.json()}
    assert riesgos == {
        "Baja": "Bajo",
        "Media": "Medio",
        "Alta": "Alto",
        "Crítica": "Crítico",
    }


# ---------- Usuarios ----------
def test_crear_usuario(client):
    r = client.post(
        "/usuarios",
        json={"nombre": "María López", "correo": "maria@empresa.com", "departamento": "RRHH"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["id"] >= 1
    assert data["nombre"] == "María López"
    assert data["departamento"] == "RRHH"


def test_crear_usuario_correo_duplicado(client, usuario):
    r = client.post("/usuarios", json={"nombre": "Otro", "correo": usuario["correo"]})
    assert r.status_code == 409


def test_crear_usuario_correo_invalido(client):
    r = client.post("/usuarios", json={"nombre": "Sin Correo", "correo": "esto-no-es-un-correo"})
    assert r.status_code == 422


def test_crear_usuario_nombre_vacio(client):
    r = client.post("/usuarios", json={"nombre": "   ", "correo": "vacio@empresa.com"})
    assert r.status_code == 422


def test_listar_usuarios(client, usuario):
    r = client.get("/usuarios")
    assert r.status_code == 200
    assert [u["id"] for u in r.json()] == [usuario["id"]]


# ---------- Técnicos ----------
def test_crear_tecnico(client):
    r = client.post(
        "/tecnicos",
        json={"nombre": "Pedro Ruiz", "correo": "pedro@soporte.com", "especialidad": "Hardware"},
    )
    assert r.status_code == 201
    assert r.json()["especialidad"] == "Hardware"


def test_crear_tecnico_correo_duplicado(client, tecnico):
    r = client.post("/tecnicos", json={"nombre": "Otro", "correo": tecnico["correo"]})
    assert r.status_code == 409


def test_listar_tecnicos(client, tecnico):
    r = client.get("/tecnicos")
    assert r.status_code == 200
    assert [t["id"] for t in r.json()] == [tecnico["id"]]