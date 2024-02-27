import uuid

from pda.seedwork.application.queries import Query, QueryHandler, QueryResult


class GetUser(Query):
    listing_id: uuid.UUID


class GetUserHandler(QueryHandler):
    def handle(self, query: Query) -> QueryResult:
        pass
