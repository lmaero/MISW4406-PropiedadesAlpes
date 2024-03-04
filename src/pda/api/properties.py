import json

from flask import Response, session
from flask import request

import pda.seedwork.presentation.api as api
from pda.modules.properties.application.commands.create_transaction import (
    CreateTransaction,
)
from pda.modules.properties.application.mappers import TransactionMapperDTOJson
from pda.modules.properties.application.queries.get_transaction import GetTransaction
from pda.seedwork.application.commands import execute_command
from pda.seedwork.application.queries import execute_query
from pda.seedwork.domain.exceptions import DomainException

bp = api.create_blueprint("properties", "/properties")


@bp.route("/transactions", methods=("POST",))
def create_transaction_command():
    try:
        session["uow_method"] = "pulsar"

        transaction_data = request.json

        transaction_mapper = TransactionMapperDTOJson()
        transaction_dto = transaction_mapper.external_to_dto(transaction_data)

        command = CreateTransaction(
            transaction_dto.id,
            transaction_dto.created_at,
            transaction_dto.updated_at,
            transaction_dto.leases,
        )

        execute_command(command)

        return Response("{}", status=202, mimetype="application/json")
    except DomainException as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )


@bp.route("/transaction", methods=("GET",))
@bp.route("/transaction/<identifier>", methods=("GET",))
def get_transaction_query_by_id(identifier=None):
    if identifier:
        query_result = execute_query(GetTransaction(identifier))
        transaction_mapper = TransactionMapperDTOJson()

        return transaction_mapper.dto_to_external(query_result.result)
    else:
        return [{"message": "GET!"}]
