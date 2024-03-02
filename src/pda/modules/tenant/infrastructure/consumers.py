import logging
import traceback

import _pulsar
import pulsar
from pulsar.schema import *

from pda.modules.tenant.infrastructure.schema.v1.commands import (
    CreateTenantCommand,
)
from pda.modules.tenant.infrastructure.schema.v1.events import (
    CreatedTenantEvent,
)
from pda.seedwork.infrastructure import utils


def subscribe_to_events():
    client = None
    try:
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumer = client.subscribe(
            "tenant-events",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="pda-sub-events",
            schema=AvroSchema(CreatedTenantEvent),
        )

        while True:
            message = consumer.receive()
            print(f"Received Event: {message.value().data}")

            consumer.acknowledge(message)

    except:
        logging.error("ERROR: Cannot subscribe to events topic")
        traceback.print_exc()
        if client:
            client.close()


def subscribe_to_commands():
    client = None
    try:
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumer = client.subscribe(
            "tenant-commands",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="pda-sub-commands",
            schema=AvroSchema(CreateTenantCommand),
        )

        while True:
            message = consumer.receive()
            print(f"Received Command: {message.value().data}")

            consumer.acknowledge(message)

    except:
        logging.error("ERROR: Cannot subscribe to commands topic")
        traceback.print_exc()
        if client:
            client.close()
