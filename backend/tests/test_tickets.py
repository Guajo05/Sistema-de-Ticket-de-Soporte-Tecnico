from datetime import datetime


def _fecha(texto: str) -> datetime:
    return datetime.fromisoformat(texto)


# ---------- Crear ----------
def test_crear_ticket(crear_ticket, usuario):
    r = crear_ticket()
    assert r.status_code == 201
    data = r.json()
    assert data["id"] >= 1
    assert data["titulo"] == "No imprime"
    assert data["estado"]["nombre"] == "Abierto"  # todo ticket nuevo nace Abierto
    assert data["urgencia"]["nombre"] == "Media"
    assert data["usuario"]["id"] == usuario["id"]
    assert data["tecnico"] is None


def test_crear_ticket_con_tecnico(crear_ticket, tecnico):
    r = crear_ticket(tecnico_id=tecnico["id"])
    assert r.status_code == 201
    assert r.json()["tecnico"]["id"] == tecnico["id"]


def test_crear_ticket_titulo_vacio(crear_ticket):
    r = crear_ticket(titulo="   ")
    assert r.status_code == 422


def test_crear_ticket_descripcion_vacia(crear_ticket):
    r = crear_ticket(descripcion="")
    assert r.status_code == 422


def test_crear_ticket_sin_campos_obligatorios(client):
    r = client.post("/tickets", json={"titulo": "Incompleto"})
    assert r.status_code == 422


def test_crear_ticket_usuario_inexistente(crear_ticket):
    r = crear_ticket(usuario_id=9999)
    assert r.status_code == 400


def test_crear_ticket_urgencia_inexistente(crear_ticket):
    r = crear_ticket(urgencia_ticket_id=999)
    assert r.status_code == 400


def test_crear_ticket_tecnico_inexistente(crear_ticket):
    r = crear_ticket(tecnico_id=9999)
    assert r.status_code == 400


# ---------- Consultar ----------
def test_listar_tickets_vacio(client):
    r = client.get("/tickets")
    assert r.status_code == 200
    assert r.json() == []


def test_listar_tickets_mas_reciente_primero(client, crear_ticket):
    primero = crear_ticket(titulo="Primero").json()
    segundo = crear_ticket(titulo="Segundo").json()
    r = client.get("/tickets")
    assert r.status_code == 200
    assert [t["id"] for t in r.json()] == [segundo["id"], primero["id"]]


def test_obtener_ticket(client, crear_ticket):
    creado = crear_ticket().json()
    r = client.get(f"/tickets/{creado['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == creado["id"]


def test_obtener_ticket_inexistente(client):
    r = client.get("/tickets/9999")
    assert r.status_code == 404


def test_filtrar_por_estado(client, crear_ticket, estados):
    t1 = crear_ticket(titulo="Uno").json()
    crear_ticket(titulo="Dos")
    client.patch(f"/tickets/{t1['id']}", json={"estado_ticket_id": estados["En progreso"]})

    r = client.get("/tickets", params={"estado_id": estados["En progreso"]})
    assert r.status_code == 200
    assert [t["id"] for t in r.json()] == [t1["id"]]


def test_filtrar_por_urgencia(client, crear_ticket, urgencias):
    crear_ticket(titulo="Normal")
    critico = crear_ticket(titulo="Urgente", urgencia_ticket_id=urgencias["Crítica"]).json()

    r = client.get("/tickets", params={"urgencia_id": urgencias["Crítica"]})
    assert r.status_code == 200
    assert [t["id"] for t in r.json()] == [critico["id"]]


def test_filtrar_por_tecnico(client, crear_ticket, tecnico):
    crear_ticket(titulo="Sin asignar")
    asignado = crear_ticket(titulo="Asignado", tecnico_id=tecnico["id"]).json()

    r = client.get("/tickets", params={"tecnico_id": tecnico["id"]})
    assert r.status_code == 200
    assert [t["id"] for t in r.json()] == [asignado["id"]]


# ---------- Actualizar ----------
def test_actualizar_estado_y_asignar_tecnico(client, crear_ticket, estados, tecnico):
    ticket = crear_ticket().json()

    r = client.patch(
        f"/tickets/{ticket['id']}",
        json={"estado_ticket_id": estados["En progreso"], "tecnico_id": tecnico["id"]},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["estado"]["nombre"] == "En progreso"
    assert data["tecnico"]["id"] == tecnico["id"]
    assert _fecha(data["fecha_actualizacion"]) > _fecha(ticket["fecha_actualizacion"])


def test_actualizar_solo_titulo_no_toca_lo_demas(client, crear_ticket):
    ticket = crear_ticket().json()

    r = client.patch(f"/tickets/{ticket['id']}", json={"titulo": "Impresora dañada"})
    assert r.status_code == 200
    data = r.json()
    assert data["titulo"] == "Impresora dañada"
    assert data["descripcion"] == ticket["descripcion"]
    assert data["estado"]["nombre"] == "Abierto"


def test_desasignar_tecnico(client, crear_ticket, tecnico):
    ticket = crear_ticket(tecnico_id=tecnico["id"]).json()

    r = client.patch(f"/tickets/{ticket['id']}", json={"tecnico_id": None})
    assert r.status_code == 200
    assert r.json()["tecnico"] is None


def test_actualizar_campo_obligatorio_con_null(client, crear_ticket):
    ticket = crear_ticket().json()

    r = client.patch(f"/tickets/{ticket['id']}", json={"estado_ticket_id": None})
    assert r.status_code == 422


def test_actualizar_estado_inexistente(client, crear_ticket):
    ticket = crear_ticket().json()

    r = client.patch(f"/tickets/{ticket['id']}", json={"estado_ticket_id": 999})
    assert r.status_code == 400


def test_actualizar_ticket_inexistente(client):
    r = client.patch("/tickets/9999", json={"titulo": "Nada"})
    assert r.status_code == 404


# ---------- Eliminar ----------
def test_eliminar_ticket(client, crear_ticket):
    ticket = crear_ticket().json()

    r = client.delete(f"/tickets/{ticket['id']}")
    assert r.status_code == 204

    assert client.get(f"/tickets/{ticket['id']}").status_code == 404


def test_eliminar_ticket_inexistente(client):
    r = client.delete("/tickets/9999")
    assert r.status_code == 404