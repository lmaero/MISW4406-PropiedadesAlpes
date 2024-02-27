import datetime

import pulsar
from pulsar.schema import *

from pda.modules.properties.infrastructure.schema.v1.commands import (
    CreateTransactionCommand,
    CreateTransactionPayloadCommand,
)
from pda.modules.properties.infrastructure.schema.v1.events import (
    CreatedTransactionEvent,
    TransactionCreatedPayload,
)
from pda.seedwork.infrastructure import utils

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Dispatcher:
    def _publish_message(self, message, topic, schema):
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publisher = client.create_producer(
            topic, schema=AvroSchema(CreatedTransactionEvent)
        )
        publisher.send(message)
        client.close()

    def publish_event(self, event, topic):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = TransactionCreatedPayload(
            id_transaction=str(event.id_transaction),
            id_client=str(event.id_client),
            created_at=int(unix_time_millis(event.created_at)),
        )
        integration_event = CreatedTransactionEvent(data=payload)
        self._publish_message(
            integration_event, topic, AvroSchema(CreatedTransactionEvent)
        )

    def publish_command(self, command, topic):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = CreateTransactionPayloadCommand(
            id_user=str(command.id_user)
            # add leases
        )
        integration_command = CreateTransactionCommand(data=payload)
        self._publish_message(
            integration_command, topic, AvroSchema(CreateTransactionCommand)
        )
