import uuid
from dataclasses import dataclass, field

import pda.modules.properties.domain.value_objects as ov
from pda.modules.properties.domain.events import (
    CreatedProperty,
    ReservaAprobada,
    LeasedProperty,
    ReservaPagada,
)
from pda.seedwork.domain.entities import RootAggregation


@dataclass
class Property(RootAggregation):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoReserva = field(default=ov.EstadoReserva.PENDIENTE)
    itinerarios: list[ov.Tenant] = field(default_factory=list[ov.Tenant])

    def crear_reserva(self, reserva: Reserva):
        self.id_cliente = reserva.id_cliente
        self.estado = reserva.estado
        self.itinerarios = reserva.tenants

        self.agregar_evento(
            CreatedProperty(
                id_reserva=self.id,
                id_cliente=self.id_cliente,
                estado=self.estado.name,
                fecha_creacion=self.fecha_creacion,
            )
        )

    def aprobar_reserva(self):
        self.estado = ov.EstadoReserva.APROBADA

        self.agregar_evento(ReservaAprobada(self.id, self.fecha_actualizacion))

    def cancelar_reserva(self):
        self.estado = ov.EstadoReserva.CANCELADA

        self.agregar_evento(LeasedProperty(self.id, self.fecha_actualizacion))

    def pagar_reserva(self):
        self.estado = ov.EstadoReserva.PAGADA

        self.agregar_evento(ReservaPagada(self.id, self.fecha_actualizacion))
