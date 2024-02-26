import json

from flask import Response
from flask import request

import pda.seedwork.presentation.api as api
from pda.modules.properties.application.mapeadores import \
    TransactionMapperDTOJson
from pda.modules.properties.application.servicios import TransactionService
from pda.seedwork.domain.exceptions import DomainException

bp = api.crear_blueprint("properties", "/properties")


@bp.route("/transactions", methods=("POST",))
def create_transaction():
    try:
        transaction_data = request.json

        transaction_mapper = TransactionMapperDTOJson()
        transaction_dto = transaction_mapper.external_to_dto(transaction_data)

        sr = TransactionService()
        final_dto = sr.create_transaction(transaction_dto)

        return transaction_mapper.dto_to_external(final_dto)
    except DomainException as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )


@bp.route("/reserva", methods=("GET",))
@bp.route("/reserva/<id>", methods=("GET",))
def dar_reserva(id=None):
    if id:
        sr = TransactionService()

        return sr.get_transaction_by_id(id)
    else:
        return [{"message": "GET!"}]
