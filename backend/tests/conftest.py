import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Carga backend/.env para poder leer TEST_DATABASE_URL en local.
# En CI la variable viene del entorno del workflow.
load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    pytest.exit(
        "Falta la variable TEST_DATABASE_URL (BD exclusiva para tests). "
        "Revisa backend/.env.example",
        returncode=2,
    )

nombre_bd = TEST_DATABASE_URL.rsplit("/", 1)[-1].split("?")[0].lower()
if "test" not in nombre_bd:
    pytest.exit(
        f"Por seguridad, la BD de tests debe tener 'test' en el nombre (es '{nombre_bd}').",
        returncode=2,
    )

# La app lee DATABASE_URL: la apuntamos a la BD de tests ANTES de importarla
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from fastapi.testclient import TestClient  # noqa: E402

from app.database import engine  # noqa: E402
from app.main import app  # noqa: E402

CARPETA_DATABASE = Path(__file__).resolve().parents[2] / "database"


@pytest.fixture(scope="session", autouse=True)
def preparar_bd():
    """Recrea el esquema desde los scripts SQL reales (la BD es la fuente de verdad)."""
    with engine.begin() as conn:
        conn.exec_driver_sql("DROP SCHEMA public CASCADE")
        conn.exec_driver_sql("CREATE SCHEMA public")
        for nombre in ("01-init.sql", "02-seed.sql", "03-add-riesgo-urgencias.sql"):
            sql = (CARPETA_DATABASE / nombre).read_text(encoding="utf-8-sig")
            conn.exec_driver_sql(sql)
    yield
    engine.dispose()


@pytest.fixture(autouse=True)
def limpiar_tablas():
    """Cada test arranca con tickets, usuarios y técnicos vacíos (los catálogos se conservan)."""
    with engine.begin() as conn:
        conn.exec_driver_sql(
            "TRUNCATE tickets, usuarios, tecnicos RESTART IDENTITY CASCADE"
        )
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def estados(client):
    """Diccionario {nombre: id}, ej. estados['Abierto']"""
    return {e["nombre"]: e["id"] for e in client.get("/estados").json()}


@pytest.fixture
def urgencias(client):
    return {u["nombre"]: u["id"] for u in client.get("/urgencias").json()}


@pytest.fixture
def usuario(client):
    r = client.post(
        "/usuarios",
        json={"nombre": "Juan Pérez", "correo": "juan@empresa.com", "departamento": "Contabilidad"},
    )
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def tecnico(client):
    r = client.post(
        "/tecnicos",
        json={"nombre": "Ana Gómez", "correo": "ana@soporte.com", "especialidad": "Redes"},
    )
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def crear_ticket(client, usuario, urgencias):
    """Devuelve una función que crea un ticket válido; se le puede sobreescribir cualquier campo."""

    def _crear(**cambios):
        datos = {
            "titulo": "No imprime",
            "descripcion": "La impresora del 2do piso no responde",
            "urgencia_ticket_id": urgencias["Media"],
            "usuario_id": usuario["id"],
        }
        datos.update(cambios)
        return client.post("/tickets", json=datos)

    return _crear