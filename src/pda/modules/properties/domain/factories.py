from dataclasses import dataclass

from pda.seedwork.domain.entities import Entity
from pda.seedwork.domain.factories import Factory
from pda.seedwork.domain.repositories import Mapper
from .entities import Property
from .exceptions import FactoryTypeNotFoundException
from .rules import MinimoUnItinerario, RutaValida


@dataclass
class _TransactionFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        else:
            property: Property = mapper.dto_to_entity(obj)

            # self.validar_regla(MinimoUnItinerario(reserva.itinerarios))
            # [
            #     self.validar_regla(RutaValida(ruta))
            #     for itin in reserva.itinerarios
            #     for odo in itin.odos
            #     for segmento in odo.segmentos
            #     for ruta in segmento.legs
            # ]

            return property


@dataclass
class PropertyFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if mapper.obtener_tipo() == Property.__class__:
            transaction_factory = _TransactionFactory()
            return transaction_factory.create_object(obj, mapper)
        else:
            raise FactoryTypeNotFoundException()
