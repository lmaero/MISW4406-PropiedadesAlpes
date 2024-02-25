from dataclasses import dataclass
from pda.seedwork.application.queries import Query, QueryResponse
from src.pda.modules.properties.application.queries.base import TransactionQueryBaseHandler

@dataclass
class GetProperty(Query):
    id: str

class GetPropertyHandler(TransactionQueryBaseHandler):
    def handle(self, query: GetProperty) -> QueryResponse:
        transaction = self.property_factory.create_object