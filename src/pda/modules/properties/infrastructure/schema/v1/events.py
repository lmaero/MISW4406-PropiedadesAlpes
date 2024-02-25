from pulsar.schema import *
from pda.seedwork.infrastructure.schema.v1.events import IntegrationEvent

class CreateTransactionPayload(Record):
    id = String()

class EventCreateTransaction(IntegrationEvent):
    data = CreateTransactionPayload()