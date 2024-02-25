from dataclasses import dataclass
from pda.seedwork.application.queries import Query, QueryResponse
from pda.seedwork.application.queries import exec_query as query
from pda.modules.properties.infrastructure.repositories import TransactionRepository
from src.pda.modules.properties.application.mappers import TransactionMapper
from src.pda.modules.properties.application.queries.base import TransactionQueryBaseHandler

@dataclass
class GetProperty(Query):
    id: str

class GetPropertyHandler(TransactionQueryBaseHandler):
    def handle(self, query: GetProperty) -> QueryResponse:
        repository = self.repository_factory.create_object(TransactionRepository)
        transaction = self.property_factory.create_object(repository.get_by_id(query.id), TransactionMapper())
        return QueryResponse(result=transaction)

@query.register(GetProperty)
def exec_query_get_property(query: GetProperty):
    handler = GetPropertyHandler()
    return handler.handle(query)