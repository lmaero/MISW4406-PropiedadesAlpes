from pda.modules.properties.domain.entidades import Itinerario, Proveedor
from pda.modules.properties.domain.mixins import FiltradoItinerariosMixin
from pda.modules.properties.domain.objetos_valor import Odo, ParametroBusca
from pda.modules.properties.domain.reglas import MinimoUnAdulto, ValidPayment
from pda.modules.properties.domain.repositorios import ProvidersRepository as rp
from pda.seedwork.domain.servicios import Servicio


class ServicioBusqueda(Servicio, FiltradoItinerariosMixin):

    def buscar_itinerarios(
        self, odos: list[Odo], parametros: ParametroBusca
    ) -> list[Itinerario]:
        itinerarios: list[Itinerario] = list()
        proveedores: list[Proveedor] = rp.get_all()

        self.validate_rule(MinimoUnAdulto(parametros.pasajeros))
        [
            self.validate_rule(ValidPayment(ruta))
            for odo in odos
            for segmento in odo.segmentos
            for ruta in segmento.legs
        ]

        itinerarios.append(
            [
                proveedor.obtener_itinerarios(odos, parametros)
                for proveedor in proveedores
            ]
        )

        return self.filtrar_mejores_itinerarios(itinerarios)
