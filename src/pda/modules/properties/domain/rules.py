from pda.seedwork.domain.rules import BusinessRule
from .entities import Pasajero
from .value_objects import Ruta
from .value_objects import TipoPasajero, Tenant


class MinimoUnAdulto(BusinessRule):

    pasajeros: list[Pasajero]

    def __init__(
        self, pasajeros, mensaje="Al menos un adulto debe ser parte del itinerario"
    ):
        super().__init__(mensaje)
        self.pasajeros = pasajeros

    def es_valido(self) -> bool:
        for pasajero in self.pasajeros:
            if pasajero.tipo == TipoPasajero.ADULTO:
                return True
        return False


class RutaValida(ReglaNegocio):

    ruta: Ruta

    def __init__(self, ruta, mensaje="La ruta propuesta es incorrecta"):
        super().__init__(mensaje)
        self.ruta = ruta

    def es_valido(self) -> bool:
        return self.ruta.destino != self.ruta.origen


class MinimoUnItinerario(ReglaNegocio):
    itinerarios: list[Tenant]

    def __init__(
        self,
        itinerarios,
        mensaje="La lista de itinerarios debe tener al menos un itinerario",
    ):
        super().__init__(mensaje)
        self.itinerarios = itinerarios

    def es_valido(self) -> bool:
        return len(self.itinerarios) > 0 and isinstance(self.itinerarios[0], Tenant)
