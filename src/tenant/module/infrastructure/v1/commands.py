import uuid

from pulsar.schema import *

from tenant.module.infrastructure.v1 import TenantType
from tenant.seedwork.infrastructure.schema.v1.commands import IntegrationCommand
from tenant.seedwork.infrastructure.utils import time_millis


class RegisterTenant(Record):
    name = String()
    last_name = String()
    email = String()
    tenant_type = TenantType
    created_date = Long()


class ValidateTenant(Record):
    id = String()
    validation_date = Long()


class DeactivateTenant(Record):
    id = String()
    deactivated_date = Long()


class CommandRegisterTenant(IntegrationCommand):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String(default="v1")
    type = String(default="RegisterTenant")
    data_content_type = String()
    service_name = String(default="tenant.pda")
    data = RegisterTenant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CommandValidateTenant(IntegrationCommand):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String(default="v1")
    type = String(default="ValidateTenant")
    data_content_type = String()
    service_name = String(default="tenant.pda")
    data = ValidateTenant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CommandDeactivateTenant(IntegrationCommand):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String(default="v1")
    type = String(default="DeactivateTenant")
    data_content_type = String()
    service_name = String(default="tenant.pda")
    data = DeactivateTenant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
