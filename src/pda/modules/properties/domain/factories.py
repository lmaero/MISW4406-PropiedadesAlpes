from dataclasses import dataclass

from pda.seedwork.domain.entities import Entity
from pda.seedwork.domain.factories import Factory
from pda.seedwork.domain.repositories import Mapper
from .entities import Reserva
from .exceptions import FactoryTypeNotFoundException
from .rules import MinimoUnItinerario, RutaValida


@dataclass
class _FactoryReserva(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        else:
            reserva: Reserva = mapper.dto_to_entity(obj)

            self.validar_regla(MinimoUnItinerario(reserva.itinerarios))
            [
                self.validar_regla(RutaValida(ruta))
                for itin in reserva.itinerarios
                for odo in itin.odos
                for segmento in odo.segmentos
                for ruta in segmento.legs
            ]

            return reserva


@dataclass
class FactoryVuelos(Factory):
    def create_object(self, obj: any, mapper: Mapeador) -> any:
        if mapper.obtener_tipo() == Reserva.__class__:
            fabrica_reserva = _FactoryReserva()
            return fabrica_reserva.create_object(obj, mapper)
        else:
            raise FactoryTypeNotFoundException()
