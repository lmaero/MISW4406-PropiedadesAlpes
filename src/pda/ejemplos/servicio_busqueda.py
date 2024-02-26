from pda.modules.properties.domain.entidades import Proveedor
from pda.modules.properties.domain.objetos_valor import (
    Odo,
    ParametroBusca,
    Lease,
)


def filtrar_mejores_itinerarios(itinerarios: list[Lease]) -> list[Lease]:
    # Logica compleja para filtrar itinerarios
    ...
    return itinerarios


def buscar_itinerarios(odos: list[Odo], parametros: ParametroBusca) -> list[Lease]:
    itinerarios: list[Lease] = list()
    proveedores: list[Proveedor] = rp.get_all()

    itinerarios.append(
        [proveedor.obtener_itinerarios(odos, parametros) for proveedor in proveedores]
    )

    return filtrar_mejores_itinerarios(itinerarios)


# origen=Aeropuerto(codigo=CodigoIATA(codigo="CPT"), nombre="Cape Town International")
# destino=Aeropuerto(codigo=CodigoIATA(codigo="JFK"), nombre="JFK International Airport")
# legs=[Leg(origen=origen, destino=destino)]
# segmentos = [Segmento(legs)]
# ruta = Odo(segmentos=segmentos)
# itinerarios = buscar_itinerarios(ruta, ParametroBusca(pasajeros=list()))
# print(itinerarios)
