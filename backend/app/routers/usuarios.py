from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[schemas.UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.scalars(select(models.Usuario).order_by(models.Usuario.nombre)).all()


@router.post("", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.scalar(select(models.Usuario).where(models.Usuario.correo == payload.correo))
    if existe:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese correo")

    usuario = models.Usuario(**payload.model_dump())
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario