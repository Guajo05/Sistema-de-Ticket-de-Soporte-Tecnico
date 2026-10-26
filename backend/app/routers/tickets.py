from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/tickets", tags=["Tickets"])

# Campos que en la BD son NOT NULL: no se pueden poner en null desde el PATCH
CAMPOS_NO_NULOS = ("titulo", "descripcion", "estado_ticket_id", "urgencia_ticket_id")


def _validar_referencias(
    db: Session,
    *,
    estado_id: Optional[int] = None,
    urgencia_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    tecnico_id: Optional[int] = None,
) -> None:
    """Devuelve 400 con un mensaje claro si algún id no existe (en vez de un error 500)."""
    if estado_id is not None and db.get(models.EstadoTicket, estado_id) is None:
        raise HTTPException(status_code=400, detail="El estado indicado no existe")
    if urgencia_id is not None and db.get(models.UrgenciaTicket, urgencia_id) is None:
        raise HTTPException(status_code=400, detail="La urgencia indicada no existe")
    if usuario_id is not None and db.get(models.Usuario, usuario_id) is None:
        raise HTTPException(status_code=400, detail="El usuario indicado no existe")
    if tecnico_id is not None and db.get(models.Tecnico, tecnico_id) is None:
        raise HTTPException(status_code=400, detail="El técnico indicado no existe")


def _obtener_ticket(db: Session, ticket_id: int) -> models.Ticket:
    ticket = db.get(models.Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket


@router.get("", response_model=list[schemas.TicketOut])
def listar_tickets(
    estado_id: Optional[int] = Query(default=None),
    urgencia_id: Optional[int] = Query(default=None),
    usuario_id: Optional[int] = Query(default=None),
    tecnico_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    consulta = select(models.Ticket).order_by(models.Ticket.id.desc())
    if estado_id is not None:
        consulta = consulta.where(models.Ticket.estado_ticket_id == estado_id)
    if urgencia_id is not None:
        consulta = consulta.where(models.Ticket.urgencia_ticket_id == urgencia_id)
    if usuario_id is not None:
        consulta = consulta.where(models.Ticket.usuario_id == usuario_id)
    if tecnico_id is not None:
        consulta = consulta.where(models.Ticket.tecnico_id == tecnico_id)
    return db.scalars(consulta).all()


@router.get("/{ticket_id}", response_model=schemas.TicketOut)
def obtener_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return _obtener_ticket(db, ticket_id)


@router.post("", response_model=schemas.TicketOut, status_code=status.HTTP_201_CREATED)
def crear_ticket(payload: schemas.TicketCreate, db: Session = Depends(get_db)):
    _validar_referencias(
        db,
        urgencia_id=payload.urgencia_ticket_id,
        usuario_id=payload.usuario_id,
        tecnico_id=payload.tecnico_id,
    )

    # Todo ticket nuevo nace en estado "Abierto"
    estado_abierto = db.scalar(
        select(models.EstadoTicket).where(models.EstadoTicket.nombre == "Abierto")
    )
    if estado_abierto is None:
        raise HTTPException(
            status_code=500,
            detail="Falta el estado 'Abierto' en la BD. Ejecuta database/02-seed.sql",
        )

    ticket = models.Ticket(**payload.model_dump(), estado_ticket_id=estado_abierto.id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.patch("/{ticket_id}", response_model=schemas.TicketOut)
def actualizar_ticket(
    ticket_id: int, payload: schemas.TicketUpdate, db: Session = Depends(get_db)
):
    ticket = _obtener_ticket(db, ticket_id)
    cambios = payload.model_dump(exclude_unset=True)

    for campo in CAMPOS_NO_NULOS:
        if campo in cambios and cambios[campo] is None:
            raise HTTPException(status_code=422, detail=f"El campo '{campo}' no puede ser null")

    _validar_referencias(
        db,
        estado_id=cambios.get("estado_ticket_id"),
        urgencia_id=cambios.get("urgencia_ticket_id"),
        tecnico_id=cambios.get("tecnico_id"),
    )

    for campo, valor in cambios.items():
        setattr(ticket, campo, valor)

    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = _obtener_ticket(db, ticket_id)
    db.delete(ticket)
    db.commit()