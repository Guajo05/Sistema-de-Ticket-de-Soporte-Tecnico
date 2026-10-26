from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/tecnicos", tags=["Técnicos"])

@router.get("", response_model=list[schemas.TecnicoOut])
def listar_tecnicos(db: Session = Depends(get_db)):
    return db.scalars(select(models.Tecnico).order_by(models.Tecnico.nombre)).all()

@router.post("", response_model=schemas.TecnicoOut, status_code=status.HTTP_201_CREATED)
def crear_tecnico(payload: schemas.TecnicoCreate, db: Session = Depends(get_db)):
    existe = db.scalar(select(models.Tecnico).where(models.Tecnico.correo == payload.correo))
    if existe:
        raise HTTPException(status_code=409, detail="Ya existe un técnico con ese correo")

    tecnico = models.Tecnico(**payload.model_dump())
    db.add(tecnico)
    db.commit()
    db.refresh(tecnico)
    return tecnico