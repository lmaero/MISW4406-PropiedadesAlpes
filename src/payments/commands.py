import uuid

from pulsar.schema import *

from .utils import time_millis


class PayTransactionPayload(Record):
    correlation_id = (String(),)
    transaction_id = (String(),)
    amount = Double()
    amount_vat = Double()
    creation_date = Long()


class ReversePaymentPayload(Record):
    id = String()
    correlation_id = String()
    transaction_id = String()


class CommandPayTransaction(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String(default="v1")
    type = String(default="CommandPayTransaction")
    data_content_type = String()
    service_name = String(default="payments.pda")
    data = PayTransactionPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CommandReversePayment(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String(default="v1")
    type = String(default="CommandReversePayment")
    data_content_type = String()
    service_name = String(default="payments.pda")
    data = ReversePaymentPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
