from tenant.seedwork.application.queries import Query, QueryHandler, QueryResult
import uuid

class GetTenant(Query):
    listing_id: uuid.UUID

class GetTenantHandler(QueryHandler):

    def handle() -> QueryResult:
        ...