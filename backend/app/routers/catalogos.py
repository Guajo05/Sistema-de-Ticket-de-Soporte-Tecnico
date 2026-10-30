from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Catálogos"])

@router.get("/estados", response_model=list[schemas.EstadoTicketOut])
def listar_estados(db: Session = Depends(get_db)):
    return db.scalars(select(models.EstadoTicket)).all()

@router.get("/urgencias", response_model=list[schemas.UrgenciaTicketOut])
def listar_urgencias(db: Session = Depends(get_db)):
    return db.scalars(select(models.UrgenciaTicket)).all()

@router.get("/riesgos", response_model=list[schemas.RiesgoTicketOut])
def listar_riesgos(db: Session = Depends(get_db)):
    return db.scalars(select(models.RiesgoTicket)).all()