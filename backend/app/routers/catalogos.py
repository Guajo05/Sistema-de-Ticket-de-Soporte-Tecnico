from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Catálogos"])

@router.get("/estados", response_model=list[schemas.EstadoOut])
def listar_estados(db: Session = Depends(get_db)):
    return db.scalars(select(models.EstadoTicket).order_by(models.EstadoTicket.id)).all()

@router.get("/urgencias", response_model=list[schemas.UrgenciaOut])
def listar_urgencias(db: Session = Depends(get_db)):
    return db.scalars(select(models.UrgenciaTicket).order_by(models.UrgenciaTicket.id)).all()