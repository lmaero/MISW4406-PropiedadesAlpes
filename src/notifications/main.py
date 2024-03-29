import os
import time
import uuid

import pulsar
from pulsar.schema import *


def time_millis():
    return int(time.time() * 1000)


class IntegrationEvent(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String()
    type = String()
    data_content_type = String()
    service_name = String()


class TransactionCreatedPayload(Record):
    id_transaction = String()
    id_client = String()
    created_at = Long()
    updated_at = Long()


class CreatedTransactionEvent(IntegrationEvent):
    data = TransactionCreatedPayload()


HOSTNAME = os.getenv("PULSAR_ADDRESS", default="localhost")

client = pulsar.Client(f"pulsar://{HOSTNAME}:6650")
consumer = client.subscribe(
    "notify-payments",
    subscription_name="start-transaction_notification",
)

while True:
    msg = consumer.receive()
    print("Received Message: '%s'" % msg.value())
    consumer.acknowledge(msg)
