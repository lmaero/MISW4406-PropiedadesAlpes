import pulsar

from ui.pda.utils import broker_host

client = pulsar.Client(f"pulsar://{broker_host()}:6650")
producer = client.create_producer("transactions-commands")

for i in range(10):
    producer.send(("Hello-Pulsar-%d" % i).encode("utf-8"))

client.close()
