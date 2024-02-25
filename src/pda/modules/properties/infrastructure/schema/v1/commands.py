from pulsar.schema import *
from dataclasses import dataclass, field
from pda.seedwork.infrastructure.schema.v1.commands import (IntegrationCommand)

class CommandCreateTransactionPayload(IntegrationCommand):
    id = String()
    

class CommandCreateTransaction(IntegrationCommand):
    data = CommandCreateTransactionPayload()