from pda.modules.properties.domain.value_objects import (
    Tenant,
    Odo,
)
from pda.seedwork.application.dto import Mapper as AppMap
from pda.seedwork.domain.repositories import Mapper as RepMap
from .dto import PaymentDTO, TransactionDTO, LeaseDTO
from ..domain.entities import Property


class TransactionMapperDTOJson(AppMap):
    def _process_lease(self, lease: dict) -> LeaseDTO:
        payments_dto: list[PaymentDTO] = list()

        for payment in lease.get("payments", list()):
            payments_dto.append(
                PaymentDTO(
                    payment.get("id"),
                    payment.get("amount"),
                    payment.get("date"),
                )
            )

        return LeaseDTO(payments_dto)

    def _process_transaction(self, transaction: dict) -> TransactionDTO:
        transaction_dto = TransactionDTO()
        for key, value in transaction.items():
            setattr(transaction_dto, key, value)
        return transaction_dto

    def external_to_dto(self, external: dict) -> PropertyDTO:
        property_dto = PropertyDTO()

        for tenant in external.get("tenants", list()):
            property_dto.tenants.append(self._process_lease(tenant))

        for transactions in external.get("transactions", list()):
            property_dto.transactions.append(self._process_transaction(transactions))

        return property_dto

    def dto_to_external(self, dto: PropertyDTO) -> dict:
        return dto.__dict__


class PropertyMapper(RepMap):
    _DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def _process_tenant(self, tenant_dto: PaymentDTO) -> Tenant:
        tenants = list()

        for odo_dto in tenant_dto.odos:
            segmentos = list()
            tenants.append(Odo(segmentos))

        return Tenant(tenants)

    def get_type(self) -> type:
        return Property.__class__

    def locacion_a_dict(self, locacion):
        if not locacion:
            return dict(
                codigo=None, nombre=None, fecha_actualizacion=None, fecha_creacion=None
            )

        return dict(
            codigo=locacion.codigo,
            nombre=locacion.nombre,
            fecha_actualizacion=locacion.updated_at.strftime(self._DATE_FORMAT),
            fecha_creacion=locacion.created_at.strftime(self._DATE_FORMAT),
        )

    def entity_to_dto(self, entity: Property) -> PropertyDTO:
        fecha_creacion = entity.created_at.strftime(self._DATE_FORMAT)
        fecha_actualizacion = entity.updated_at.strftime(self._DATE_FORMAT)
        _id = str(entity.id)
        itinerarios = list()

        for itin in entity.tenants:
            odos = list()
            for odo in itin.odos:
                segmentos = list()
                for seg in odo.segmentos:
                    legs = list()
                    for leg in seg.legs:
                        fecha_salida = leg.fecha_salida.strftime(self._DATE_FORMAT)
                        fecha_llegada = leg.fecha_llegada.strftime(self._DATE_FORMAT)
                        origen = self.locacion_a_dict(leg.origen)
                        destino = self.locacion_a_dict(leg.destino)
                        leg = LegDTO(
                            fecha_salida=fecha_salida,
                            fecha_llegada=fecha_llegada,
                            origen=origen,
                            destino=destino,
                        )

                        legs.append(leg)

                    segmentos.append(SegmentoDTO(legs))
                odos.append(OdoDTO(segmentos))
            itinerarios.append(PaymentDTO(odos))

        return PropertyDTO(fecha_creacion, fecha_actualizacion, _id, itinerarios)

    def dto_to_entity(self, dto: PropertyDTO) -> Property:
        property_obj = Property()
        property_obj.tenants = list()

        tenants: list[PaymentDTO] = dto.tenants

        for tenant in tenants:
            property_obj.tenants.append(self._process_tenant(tenant))

        return property_obj
