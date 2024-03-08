import logging
import traceback
import asyncio
import pulsar, _pulsar
import aiopulsar
from pulsar.schema import *
from tenant.seedwork.infrastructure import utils


async def subscribe_to_topic(topic: str, subscription: str, schema: Record, consumer_type:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as client:
            async with client.subscribe(
                topic, 
                consumer_type=consumer_type,
                subscription_name=subscription, 
                schema=AvroSchema(schema)
            ) as consumer:
                while True:
                    msg = await consumer.receive()
                    print(msg)
                    data = msg.value()
                    print(f'Received Event: {data}')
                    await consumer.acknowledge(msg)    

    except:
        logging.error('ERROR: Cannot subscribe to event topic!')
        traceback.print_exc()