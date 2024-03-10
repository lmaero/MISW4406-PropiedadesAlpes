import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from . import utils

async def suscribe_to_topic(topic: str, suscription: str, schema: str, consumer_type:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared, events=[]):
    try:
        json_schema = utils.get_schema_registry(schema)
        avro_schema = utils.get_schema_avro_from_dictionary(json_schema)
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as client:
            async with client.subscribe(
                topic,
                consumer_type=consumer_type,
                subscription_name=suscription,
                schema=avro_schema
            ) as consumer:
                while True:
                    message = await consumer.receive()
                    print(message)
                    data = message.value()
                    print(f'Evento recibido: {data}')
                    events.append(str(data))
                    await consumer.acknowledge(message)

    except:
        logging.error(f'ERROR: Suscribing to the topic! {topic}, {suscription}, {schema}')
        traceback.print_exc()