import logging
import traceback

import _pulsar
import aiopulsar
from pulsar.schema import *

from .utils import broker_host


async def subscribe_to_topic(
    topic: str,
    subscription: str,
    schema: Record,
    consumer_type: _pulsar.ConsumerType = _pulsar.ConsumerType.Shared,
):
    try:
        async with aiopulsar.connect(f"pulsar://{broker_host()}:6650") as client:
            async with client.subscribe(
                topic,
                consumer_type=consumer_type,
                subscription_name=subscription,
                schema=AvroSchema(schema),
            ) as consumer:
                while True:
                    msg = await consumer.receive()
                    print(msg)
                    data = msg.value()
                    print(f"Event received: {data}")
                    await consumer.acknowledge(msg)

    except:
        logging.error(
            f"ERROR: Cannot subscribe to events topic! {topic}, {subscription}, {schema}"
        )
        traceback.print_exc()
