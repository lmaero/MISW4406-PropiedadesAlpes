from pulsar.schema import *

from pda.seedwork.infrastructure.schema.v1.commands import IntegrationCommand


class CreateTransactionPayloadCommand(IntegrationCommand):
    id_user = String()


class CreateTransactionCommand(IntegrationCommand):
    data = CreateTransactionPayloadCommand()
