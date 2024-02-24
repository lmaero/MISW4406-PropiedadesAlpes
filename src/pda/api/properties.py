import json

from flask import request, Response

import pda.seedwork.presentation.api as api
from pda.modules.properties.application.commands.create_property import \
    CreateProperty
from pda.modules.properties.application.mappers import PropertyMapperDTOJSON
from pda.seedwork.application.commands import execute_command
from pda.seedwork.domain.exceptions import DomainException

app = api.create_blueprint("properties", "/property")


@app.route("/", methods="POST")
def create_property_async():
    try:
        property_data = request.json

        property_mapper = PropertyMapperDTOJSON()
        property_dto = property_mapper.external_to_dto(property_data)

        command = CreateProperty(
            property_dto.created_at,
            property_dto.updated_at,
            property_dto.id,
            property_dto.tenants,
            property_dto.transactions,
            property_dto.location,
            property_dto.availability,
            property_dto.size,
        )

        execute_command(command)

        return Response("{}", status=202, mimetype="application/json")
    except DomainException as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )


@app.route("/<id>", methods="GET")
def dar_reserva_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerReserva(id))
        map_reserva = MapeadorReservaDTOJson()

        return map_reserva.dto_to_external(query_resultado.resultado)
    else:
        return [{"message": "GET!"}]
