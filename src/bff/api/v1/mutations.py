import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Dispatcher

from .schemas import *


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_transaction(
        self, id_user: str, id_correlation: str, info: Info
    ) -> TransactionAnswer:
        print(f"ID User: {id_user}, ID Correlation: {id_correlation}")
        payload = dict(
            id_user=id_user,
            id_correlation=id_correlation,
            creation_date=utils.time_millis(),
        )
        command = dict(
            id=str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion="v1",
            type="TransactionCommand",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name="BFF Web",
            data=payload,
        )
        dispatcher = Dispatcher()
        info.context["background_tasks"].add_task(
            dispatcher.publicar_mensaje,
            command,
            "create-transaction-command",
            "public/default/create-transaction-command",
        )

        return TransactionAnswer(mensaje="Processing message", codigo=203)