import os
import time
from datetime import datetime

epoch = datetime.utcfromtimestamp(0)


def time_millis():
    return int(time.time() * 1000)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def millis_a_datetime(millis):
    return datetime.fromtimestamp(millis / 1000.0)


def broker_host():
    return os.getenv("PULSAR_ADDRESS", default="localhost")
