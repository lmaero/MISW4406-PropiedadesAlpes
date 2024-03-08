from pulsar.schema import *
from tenant.module.infrastructure.v1 import TenantType

class RegisteredTenant():
    id = String()
    name = String()
    last_name = String()
    email = String()
    tenant_type = TenantType
    created_date = Long()

class ValidatedTenant():
    id = String()
    validation_date = Long()

class DeactivatedTenant():
    id = String()
    deactivated_date = Long()