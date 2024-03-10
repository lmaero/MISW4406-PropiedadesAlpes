import pulsar
from pulsar.schema import *

from . import utils

class Dispatcher:
    def __init__(self):
        ...

    async def publish_message(self, message, topic, schema):
        json_schema = utils.get_schema_registry(schema)
        avro_schema = utils.get_schema_avro_from_dictionary(json_schema)

        cliente= pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publisher = cliente.create_producer(topic, schema=avro_schema)
        publisher.send(message)
        cliente.close()