import json
import os

import requests
from fastavro.schema import parse_schema
from pulsar.schema import *

PULSAR_ENV: str = "PULSAR_ADDRESS"


def broker_host():
    return os.getenv(PULSAR_ENV, default="localhost")


def retrieve_topic_schema(topic: str) -> dict:
    json_registry = requests.get(
        f"http://{broker_host()}:8080/admin/v2/schemas/{topic}/schema"
    ).json()
    return json.loads(json_registry.get("data", {}))


def parse_json_schema_to_avro(json_schema: dict) -> AvroSchema:
    schema_definition = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=schema_definition)
