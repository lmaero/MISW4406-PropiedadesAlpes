import _pulsar
import pulsar

from .utils import (
    retrieve_topic_schema,
    parse_json_schema_to_avro,
    broker_host,
)


def get_subscription_to_topic():
    json_schema = retrieve_topic_schema("public/default/transaction-events")
    avro_schema = parse_json_schema_to_avro(json_schema)

    client = pulsar.Client(f"pulsar://{broker_host()}:6650")
    return client.subscribe(
        "transaction-events",
        consumer_type=_pulsar.ConsumerType.Shared,
        subscription_name="pda-bff",
        schema=avro_schema,
    )
