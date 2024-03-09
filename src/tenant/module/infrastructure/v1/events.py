import uuid

from pulsar.schema import *

from tenant.module.infrastructure.v1 import TenantType
from tenant.seedwork.infrastructure.schema.v1.events import IntegrationEvent
from tenant.seedwork.infrastructure.utils import time_millis


class RegisteredTenant(Record):
    id = String()
    name = String()
    last_name = String()
    email = String()
    tenant_type = TenantType
    created_date = Long()


class ValidatedTenant(Record):
    id = String()
    validation_date = Long()


class DeactivatedTenant(Record):
    id = String()
    deactivated_date = Long()


class TenantEvent(IntegrationEvent):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String(default="v1")
    type = String(default="TenantEvent")
    data_content_type = String()
    service_name = String(default="tenant.pda")
    registered_tenant = RegisteredTenant
    validated_tenant = ValidatedTenant
    deactivated_tenant = DeactivatedTenant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
