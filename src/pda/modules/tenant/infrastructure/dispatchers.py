import datetime

import pulsar
from pulsar.schema import *

from pda.modules.tenant.infrastructure.schema.v1.events import (
    TenantCreatedPayload,
    CreatedTenantEvent
)

from pda.modules.tenant.infrastructure.schema.v1.commands import (
    CreateTenantPayloadCommand,
    CreateTenantCommand
)

from pda.seedwork.infrastructure import utils

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Dispatcher:
    def _publish_message(self, message, topic, schema):
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publisher = client.create_producer(
            topic, schema=AvroSchema(CreatedTenantEvent)
        )
        publisher.send(message)
        client.close()

    def publish_event(self, event, topic):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = TenantCreatedPayload(
            id_tenant=str(event.id_tenant),
            name=event.name,
            email=event.email,
            guarantorName=event.guarantorName,
            created_at=unix_time_millis(event.created_at),
            updated_at=unix_time_millis(event.updated_at),
        )
        integration_event = CreatedTenantEvent(data=payload)
        self._publish_message(
            integration_event, topic, AvroSchema(CreatedTenantEvent)
        )

    def publish_command(self, command, topic):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = CreateTenantPayloadCommand(
            id_tenant=str(command.id_tenant)
        )
        integration_command = CreateTenantCommand(data=payload)
        self._publish_message(
            integration_command, topic, AvroSchema(CreateTenantCommand)
        )
