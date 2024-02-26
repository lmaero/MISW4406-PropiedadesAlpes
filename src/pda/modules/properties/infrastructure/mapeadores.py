""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from pda.modules.properties.domain.entidades import Aeropuerto, Transaction
from pda.modules.properties.domain.objetos_valor import (
    Odo,
    Payment,
    Segmento,
    Lease,
)
from pda.seedwork.domain.repositorios import Mapper
from .dto import Lease as LeaseDTO
from .dto import Transaction as TransactionDTO


class MapperReserva(Mapper):
    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"

    def _procesar_itinerario_dto(self, itinerarios_dto: list) -> list[Lease]:
        itin_dict = dict()

        for itin in itinerarios_dto:
            destino = Aeropuerto(codigo=itin.destino_codigo, nombre=None)
            origen = Aeropuerto(codigo=itin.origen_codigo, nombre=None)
            fecha_salida = itin.fecha_salida
            fecha_llegada = itin.fecha_llegada

            itin_dict.setdefault(str(itin.payment_order), {}).setdefault(
                str(itin.segmento_orden), {}
            ).setdefault(
                str(itin.leg_orden),
                Payment(fecha_salida, fecha_llegada, origen, destino),
            )

        odos = list()
        for k, odos_dict in itin_dict.items():
            segmentos = list()
            for k, seg_dict in odos_dict.items():
                legs = list()
                for k, leg in seg_dict.items():
                    legs.append(leg)
                segmentos.append(Segmento(legs))
            odos.append(Odo(segmentos))

        return [Lease(odos)]

    def _process_lease(self, lease: any) -> list[LeaseDTO]:
        leases = list()

        for i, payment in enumerate(lease.payments):
            lease_dto = LeaseDTO()
            lease_dto.amount = payment.amount
            lease_dto.date = payment.date
            leases.append(lease_dto)

        return leases

    def get_type(self) -> type:
        return Transaction.__class__

    def entity_to_dto(self, entity: Transaction) -> TransactionDTO:
        transaction_dto = TransactionDTO()
        transaction_dto.created_at = entity.created_at
        transaction_dto.updated_at = entity.updated_at
        transaction_dto.id = str(entity.id)

        leases_dto = list()

        for lease in entity.leases:
            leases_dto.extend(self._process_lease(lease))

        transaction_dto.leases = leases_dto

        return transaction_dto

    def dto_to_entity(self, dto: TransactionDTO) -> Transaction:
        reserva = Transaction(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        reserva.leases = list()

        itinerarios_dto: list[LeaseDTO] = dto.leases

        reserva.leases.extend(self._procesar_itinerario_dto(itinerarios_dto))

        return reserva
