import json

from flask import request, Response

import pda.seedwork.presentation.api as api
from pda.modules.properties.application.commands.create_property import (
    CreateTransaction,
)
from pda.modules.properties.application.mappers import TransactionMapperDTOJson
from pda.seedwork.application.commands import execute_command
from pda.seedwork.domain.exceptions import DomainException
from src.pda.modules.properties.application.queries.get_property import GetProperty
from src.pda.seedwork.application.queries import exec_query

app = api.create_blueprint("properties", "/properties")


@app.route("/transactions", methods="POST")
def create_transaction_async():
    try:
        transaction_data = request.json

        transaction_mapper = TransactionMapperDTOJson()
        transaction_dto = transaction_mapper.external_to_dto(transaction_data)

        command = CreateTransaction(
            transaction_dto.created_at,
            transaction_dto.updated_at,
            transaction_dto.id,
            transaction_dto.tenants,
            transaction_dto.transactions,
            transaction_dto.location,
            transaction_dto.availability,
            transaction_dto.size,
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
        query_result = exec_query(GetProperty(id))
        map_transaction = TransactionMapperDTOJson()

        return map_transaction.dto_to_external(query_result.result)
    else:
        return [{"message": "GET!"}]
