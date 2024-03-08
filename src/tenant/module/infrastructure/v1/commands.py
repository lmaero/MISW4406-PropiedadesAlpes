from pulsar.schema import *
from dataclasses import dataclass, field
from tenant.seedwork.infrastructure.schema.v1.commands import (IntegrationCommand)
from tenant.seedwork.infrastructure.utils import time_millis
from tenant.module.infrastructure.v1 import TenantType
import uuid


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
    specversion = String(default="v1")
    type = String(default="RegisterTenant")
    datacontenttype = String()
    service_name = String(default="tenant.pda")
    data = RegisterTenant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CommandValidateTenant(IntegrationCommand):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="ValidateTenant")
    datacontenttype = String()
    service_name = String(default="tenant.pda")
    data = ValidateTenant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CommandDeactivateTenant(IntegrationCommand):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="DeactivateTenant")
    datacontenttype = String()
    service_name = String(default="tenant.pda")
    data = DeactivateTenant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)