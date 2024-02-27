from dataclasses import dataclass

from pda.modules.properties.application.mappers import TransactionMapper
from pda.modules.properties.infrastructure.repositories import TransactionsRepository
from pda.seedwork.application.queries import Query, QueryResult
from pda.seedwork.application.queries import execute_query as query
from .base import TransactionQueryBaseHandler


@dataclass
class GetTransaction(Query):
    id: str


class GetTransactionHandler(TransactionQueryBaseHandler):
    def handle(self, query: GetTransaction) -> QueryResult:
        transaction = self.repository_factory.create_object(
            TransactionsRepository.__class__
        )
        transaction = self.properties_factory.create_object(
            transaction.get_by_id(query.id), TransactionMapper()
        )
        return QueryResult(result=transaction)


@query.register(GetTransaction)
def execute_get_transaction_query(query: GetTransaction):
    handler = GetTransactionHandler()
    return handler.handle(query)
