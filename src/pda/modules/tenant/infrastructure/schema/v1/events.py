from pulsar.schema import *

from pda.seedwork.infrastructure.schema.v1.events import IntegrationEvent


class TenantCreatedPayload(Record):
    id_tenant = String()
    name = String()
    email = String()
    guarantorName = String()
    created_at = Long()
    updated_at = Long()


class CreatedTenantEvent(IntegrationEvent):
    data = TenantCreatedPayload()
