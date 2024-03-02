from pulsar.schema import *

from pda.seedwork.infrastructure.schema.v1.commands import IntegrationCommand


class CreateTenantPayloadCommand(IntegrationCommand):
    id_tenant = String()


class CreateTenantCommand(IntegrationCommand):
    data = CreateTenantPayloadCommand()
