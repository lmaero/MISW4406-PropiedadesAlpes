import uuid

from pulsar.schema import *

from pda.seedwork.infrastructure.schema.v1.events import IntegrationEvent
from pda.seedwork.infrastructure.utils import time_millis


class TransactionCreatedPayload(Record):
    id_transaction = String()
    id_client = String()
    created_at = Long()
    updated_at = Long()


class CreatedTransactionEvent(IntegrationEvent):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String()
    type = String()
    data_content_type = String()
    service_name = String()
    data = TransactionCreatedPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
