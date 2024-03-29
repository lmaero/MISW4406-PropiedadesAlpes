import uuid

from pulsar.schema import *

from pda.seedwork.infrastructure.utils import time_millis


class Message(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    spec_version = String()
    type = String()
    data_content_type = String()
    service_name = String()

    def __init__(self, *args, id=None, **kwargs):
        super().__init__(*args, id=id, **kwargs)
