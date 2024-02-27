from pulsar.schema import *

from pda.seedwork.infrastructure.schema.v1.events import IntegrationEvent


class TransactionCreatedPayload(Record):
    id_transaction = String()
    id_client = String()
    created_at = Long()


class CreatedTransactionEvent(IntegrationEvent):
    data = TransactionCreatedPayload()
