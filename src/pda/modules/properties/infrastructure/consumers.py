import logging
import traceback

import _pulsar
import pulsar
from pulsar.schema import *

from pda.modules.properties.infrastructure.projections import (
    TotalTransactionsProjection,
    TransactionsListProjection,
)
from pda.modules.properties.infrastructure.schema.v1.commands import (
    CreateTransactionCommand,
)
from pda.modules.properties.infrastructure.schema.v1.events import (
    CreatedTransactionEvent,
)
from pda.seedwork.infrastructure import utils
from pda.seedwork.infrastructure.projections import execute_projection


def subscribe_to_events(app=None):
    client = None
    try:
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumer = client.subscribe(
            "transaction-events",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="pda-sub-events",
            schema=AvroSchema(CreatedTransactionEvent),
        )

        while True:
            message = consumer.receive()
            data = message.value().data
            print(f"Received Event: {data}")

            execute_projection(
                TotalTransactionsProjection(
                    data.created_at, TotalTransactionsProjection.ADD
                ),
                app=app,
            )
            execute_projection(
                TransactionsListProjection(
                    data.id_transaction,
                    data.id_client,
                    data.created_at,
                    data.updated_at,
                ),
                app=app,
            )

            consumer.acknowledge(message)

    except:
        logging.error("ERROR: Cannot subscribe to events topic")
        traceback.print_exc()
        if client:
            client.close()


def subscribe_to_commands(app=None):
    client = None
    try:
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumer = client.subscribe(
            "transaction-commands",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="pda-sub-commands",
            schema=AvroSchema(CreateTransactionCommand),
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
