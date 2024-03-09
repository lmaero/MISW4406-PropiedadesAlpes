import uuid

from tenant.seedwork.application.queries import Query, QueryHandler, QueryResult


class GetTenant(Query):
    listing_id: uuid.UUID


class GetTenantHandler(QueryHandler):

    def handle() -> QueryResult: ...
