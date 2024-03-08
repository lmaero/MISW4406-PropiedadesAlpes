import pulsar
from pulsar.schema import *

from tenant.seedwork.infrastructure import utils

class Dispatcher:
    def __init__(self):
        ...

    def publish_message(self, msg, topic):
        client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publisher = client.create_producer(topic, schema=AvroSchema(msg.__class__))
        publisher.send(msg)
        client.close()