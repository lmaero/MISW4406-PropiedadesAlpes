import uuid
from dataclasses import dataclass, field

import pda.modules.properties.domain.value_objects as ov
from pda.modules.properties.domain.events import (
    CreatedProperty,
)
from pda.seedwork.domain.entities import RootAggregation


@dataclass
class Transaction(RootAggregation):
    id_property: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoReserva = field(default=ov.EstadoReserva.PENDIENTE)
    itinerarios: list[ov.Tenant] = field(default_factory=list[ov.Tenant])

    def create_transaction(self, reserva: Transaction):
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
