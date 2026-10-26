from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    correo: Mapped[str] = mapped_column(String(150), unique=True)
    departamento: Mapped[Optional[str]] = mapped_column(String(100))
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Tecnico(Base):
    __tablename__ = "tecnicos"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    correo: Mapped[str] = mapped_column(String(150), unique=True)
    especialidad: Mapped[Optional[str]] = mapped_column(String(100))
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class EstadoTicket(Base):
    __tablename__ = "estados_ticket"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(200))


class UrgenciaTicket(Base):
    __tablename__ = "urgencias_ticket"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(200))


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150))
    descripcion: Mapped[str] = mapped_column(Text)

    estado_ticket_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("estados_ticket.id")
    )
    urgencia_ticket_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("urgencias_ticket.id")
    )
    usuario_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("usuarios.id"))
    tecnico_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("tecnicos.id")
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # La BD solo pone el valor al insertar; onupdate lo renueva en cada UPDATE
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    estado: Mapped[EstadoTicket] = relationship(lazy="joined")
    urgencia: Mapped[UrgenciaTicket] = relationship(lazy="joined")
    usuario: Mapped[Usuario] = relationship(lazy="joined")
    tecnico: Mapped[Optional[Tecnico]] = relationship(lazy="joined")