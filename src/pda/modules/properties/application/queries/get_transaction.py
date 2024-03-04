from dataclasses import dataclass

from pda.modules.properties.application.mappers import TransactionMapper
from pda.modules.properties.domain.entities import Transaction
from pda.seedwork.application.queries import Query, QueryResult
from pda.seedwork.application.queries import execute_query
from .base import TransactionQueryBaseHandler


@dataclass
class GetTransaction(Query):
    id: str


class GetTransactionHandler(TransactionQueryBaseHandler):
    def handle(self, query: GetTransaction) -> QueryResult:
        view = self.view_factory.create_object(Transaction)
        transaction = self.properties_factory.create_object(
            view.get_by_id(query.id)[0], TransactionMapper()
        )
        return QueryResult(result=transaction)


@execute_query.register(GetTransaction)
def execute_get_transaction_query(query: GetTransaction):
    handler = GetTransactionHandler()
    return handler.handle(query)
