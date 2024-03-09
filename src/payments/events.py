import uuid

from pulsar.schema import *

from .utils import time_millis


class PaidTransaction(Record):
    id = (String(),)
    correlation_id = (String(),)
    transaction_id = (String(),)
    amount = Double()
    amount_vat = Double()
    creation_date = Long()


class ReversedPayment(Record):
    id = String()
    correlation_id = String()
    transaction_id = String()
    update_date = Long()


class EventPayment(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String(default="v1")
    type = String(default="EventPayment")
    data_content_type = String()
    service_name = String(default="payments.pda")
    paid_transaction = PaidTransaction
    reversed_payment = ReversedPayment

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
