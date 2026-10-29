from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import CORS_ORIGINS
from .routers import catalogos, tecnicos, tickets, usuarios

app = FastAPI(
    title="Sistema de Tickets de Soporte Técnico",
    description="API para registrar y dar seguimiento a incidencias informáticas",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets.router)
app.include_router(usuarios.router)
app.include_router(tecnicos.router)
app.include_router(catalogos.router)


@app.get("/health", tags=["Salud"])
def health():
    return {"status": "ok"}

@app.get("/", tags=["Raíz"])
def read_root():
    return {"status": "ok", "message": "API de Tickets funcionando correctamente"}