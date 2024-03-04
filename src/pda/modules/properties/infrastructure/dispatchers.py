import pulsar
from pulsar.schema import *

from pda.modules.properties.infrastructure.mappers import \
    TransactionEventsMapper
from pda.modules.properties.infrastructure.schema.v1.commands import (
    CreateTransactionCommand,
    CreateTransactionPayloadCommand,
)
from pda.seedwork.infrastructure import utils


class Dispatcher:
    def __init__(self):
        self.mapper = TransactionEventsMapper()

    def _publish_message(self, message, topic, schema):
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publisher = client.create_producer(topic, schema=schema)
        publisher.send(message)
        client.close()

    def publish_event(self, event, topic):
        event = self.mapper.entity_to_dto(event)
        self._publish_message(event, topic, AvroSchema(event.__class__))

    def publish_command(self, command, topic):
        payload = CreateTransactionPayloadCommand(
            id_user=str(command.id_user)
            # add leases
        )
        integration_command = CreateTransactionCommand(data=payload)
        self._publish_message(
            integration_command, topic, AvroSchema(CreateTransactionCommand)
        )
