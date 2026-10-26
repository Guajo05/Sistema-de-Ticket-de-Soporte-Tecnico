from datetime import datetime
from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    StringConstraints,
    field_validator,
)

Texto100 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
Texto150 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]
TextoLibre = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- Catálogos ----------
class EstadoOut(ORMModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None


class UrgenciaOut(ORMModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None


# ---------- Usuarios y técnicos ----------
class PersonaBase(BaseModel):
    nombre: Texto100
    correo: EmailStr

    @field_validator("correo")
    @classmethod
    def validar_largo_correo(cls, v: str) -> str:
        if len(v) > 150:
            raise ValueError("El correo no puede superar 150 caracteres")
        return v


class UsuarioCreate(PersonaBase):
    departamento: Optional[Texto100] = None


class UsuarioOut(ORMModel):
    id: int
    nombre: str
    correo: str
    departamento: Optional[str] = None
    fecha_creacion: datetime


class TecnicoCreate(PersonaBase):
    especialidad: Optional[Texto100] = None


class TecnicoOut(ORMModel):
    id: int
    nombre: str
    correo: str
    especialidad: Optional[str] = None
    fecha_creacion: datetime


# ---------- Tickets ----------
class TicketCreate(BaseModel):
    titulo: Texto150
    descripcion: TextoLibre
    urgencia_ticket_id: int
    usuario_id: int
    tecnico_id: Optional[int] = None


class TicketUpdate(BaseModel):
    titulo: Optional[Texto150] = None
    descripcion: Optional[TextoLibre] = None
    estado_ticket_id: Optional[int] = None
    urgencia_ticket_id: Optional[int] = None
    tecnico_id: Optional[int] = None


class TicketOut(ORMModel):
    id: int
    titulo: str
    descripcion: str
    estado: EstadoOut
    urgencia: UrgenciaOut
    usuario: UsuarioOut
    tecnico: Optional[TecnicoOut] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime