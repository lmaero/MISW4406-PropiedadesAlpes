from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from pda.seedwork.domain.events import EventDomain


@dataclass
class CreatedProperty(EventDomain):
    id_reserva: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None


@dataclass
class LeasedProperty(EventDomain):
    id_reserva: uuid.UUID = None
    fecha_actualizacion: datetime = None


@dataclass
class ReservaAprobada(EventDomain):
    id_reserva: uuid.UUID = None
    fecha_actualizacion: datetime = None


@dataclass
class ReservaPagada(EventDomain):
    id_reserva: uuid.UUID = None
    fecha_actualizacion: datetime = None
