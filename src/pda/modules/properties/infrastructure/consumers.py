import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from pda.modules.properties.infrastructure.schema.v1.commands import CommandCreateTransaction
from pda.modules.properties.infrastructure.schema.v1.events import EventCreateTransaction
from pda.seedwork.infrastructure import utils

def subscribe_to_events():
    client = None
    try:
        client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumer = client.subscribe('transaction-events', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='pda-sub-events', schema=AvroSchema(EventCreateTransaction))

        while True:
            msg = consumer.receive()
            print(f'Event Recived: {msg.value().data}')
            consumer.acknowledge(msg)     

        cliente.close()
    except:
        logging.error('ERROR: Subscribing to the events topic!')
        traceback.print_exc()
        if client:
            client.close()

def subscribe_to_commands():
    client = None
    try:
        client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumer = client.subscribe('transaction-commands', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='pda-sub-commands', schema=AvroSchema(CommandCreateTransaction))

        while True:
            msg = consumer.receive()
            print(f'Command Recived: {msg.value().data}')
            consumer.acknowledge(msg)     

        cliente.close()
    except:
        logging.error('ERROR: Subscribing to the commands topic!')
        traceback.print_exc()
        if client:
            client.close()