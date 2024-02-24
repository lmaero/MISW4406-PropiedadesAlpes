from aeroalpes.modulos.vuelos.dominio.fabricas import FabricaVuelos
from aeroalpes.modulos.vuelos.infraestructura.fabricas import FabricaRepositorio

from pda.seedwork.application.commands import CommandHandler


class CreatePropertyBaseHandler(CommandHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_vuelos: FabricaVuelos = FabricaVuelos()

    @property
    def repository_factory(self):
        return self._fabrica_repositorio

    @property
    def properties_factory(self):
        return self._fabrica_vuelos
