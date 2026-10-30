from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Prioridad = Literal["baja", "media", "alta", "critica"]
Estado = Literal["abierto", "en_progreso", "resuelto", "cerrado"]

# ==========================================
# ESQUEMAS DE CATÁLOGOS (Estados, Urgencias, Riesgos)
# ==========================================

class EstadoTicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    descripcion: Optional[str] = None

class UrgenciaTicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    descripcion: Optional[str] = None

class RiesgoTicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    descripcion: Optional[str] = None

# ==========================================
# ESQUEMAS DE USUARIOS Y TÉCNICOS
# ==========================================

class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    correo: str = Field(min_length=5, max_length=150)
    departamento: Optional[str] = Field(default=None, max_length=100)

class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    correo: str
    departamento: Optional[str] = None

class TecnicoCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    correo: str = Field(min_length=5, max_length=150)
    especialidad: Optional[str] = Field(default=None, max_length=100)

class TecnicoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    correo: str
    especialidad: Optional[str] = None

# ==========================================
# ESQUEMAS DE TICKETS
# ==========================================

class TicketCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=150)
    descripcion: str = Field(min_length=3)
    urgencia_ticket_id: int
    riesgo_ticket_id: Optional[int] = None 
    usuario_id: int
    tecnico_id: Optional[int] = None

class TicketUpdate(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=3, max_length=150)
    descripcion: Optional[str] = Field(default=None, min_length=3)
    urgencia_ticket_id: Optional[int] = None
    riesgo_ticket_id: Optional[int] = None 
    estado_ticket_id: Optional[int] = None
    tecnico_id: Optional[int] = None

class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descripcion: str

    estado: EstadoTicketOut
    urgencia: UrgenciaTicketOut
    riesgo: Optional[RiesgoTicketOut] = None 
    usuario: UsuarioOut
    tecnico: Optional[TecnicoOut] = None
    
    fecha_creacion: datetime
    fecha_actualizacion: datetime