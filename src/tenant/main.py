import asyncio

from fastapi import FastAPI, Depends
import pulsar
import json
from sqlalchemy.orm import Session

from tenant.api.v1.router import router as v1
from tenant.config.api import app_configs
from tenant.module.infrastructure.consumers import subscribe_to_topic
from tenant.module.infrastructure.dispatchers import Dispatcher
from tenant.module.infrastructure.v1 import TenantType
from tenant.module.infrastructure.v1.commands import (
    CommandRegisterTenant,
    CommandValidateTenant,
    CommandDeactivateTenant,
    RegisterTenant,
    ValidateTenant,
    DeactivateTenant,
)
from tenant.module.infrastructure.v1.events import (
    TenantEvent,
    ValidatedTenant,
    DeactivatedTenant,
    RegisteredTenant,
)
from tenant.config.db import Base, engine
from tenant.seedwork.infrastructure import utils
from tenant.config.utils import add_saga_log


app = FastAPI(**app_configs)
tasks = list()

Base.metadata.create_all(engine)
session = Session(engine)

client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
consumer = client.subscribe(
    "start-transaction",
    subscription_name="start-transaction_tenant",
)


producer = client.create_producer("pay-transaction")
rollback_producer = client.create_producer("rollback-transaction")

while True:
    msg = consumer.receive()
    msg_dict = json.loads(msg.value().decode("utf-8"))
    correlation_id = msg_dict['id']
    tenant_info = msg_dict['transaction']['tenant']
    print("Received Message: '%s'" % tenant_info)
    add_saga_log(correlation_id, "tenant-validated")
    producer.send(msg.value())
    consumer.acknowledge(msg)


@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(
        subscribe_to_topic("tenant-events", "sub-tenant", TenantEvent)
    )
    task2 = asyncio.ensure_future(
        subscribe_to_topic(
            "command-register-tenant", "sub-com-register-tenant", CommandRegisterTenant
        )
    )
    task3 = asyncio.ensure_future(
        subscribe_to_topic(
            "command-validate-tenant", "sub-com-validate-tenant", CommandValidateTenant
        )
    )
    task4 = asyncio.ensure_future(
        subscribe_to_topic(
            "command-deactivate-tenant",
            "sub-com-deactivate-tenant",
            CommandDeactivateTenant,
        )
    )
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)
    tasks.append(task4)


@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()


# Events
@app.get("/test-validated-tenant", include_in_schema=False)
async def test_validated_tenant() -> dict[str, str]:
    payload = ValidatedTenant(id="1232321321", validation_date=utils.time_millis())
    event = TenantEvent(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        data_content_type=ValidatedTenant.__name__,
        validated_tenant=payload,
    )
    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "tenant-events")
    return {"status": "ok"}


@app.get("/test-registered-tenant", include_in_schema=False)
async def test_registered_tenant() -> dict[str, str]:
    payload = RegisteredTenant(
        id="1232321321",
        name="Camilo",
        last_name="Galvez",
        email="cgalvez@uniandes.edu.co",
        tenant_type=TenantType.natural,
        created_date=utils.time_millis(),
    )
    event = TenantEvent(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        data_content_type=RegisteredTenant.__name__,
        registered_tenant=payload,
    )
    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "tenant-events")
    return {"status": "ok"}


@app.get("/test-deactivated-tenant", include_in_schema=False)
async def test_deactivated_tenant() -> dict[str, str]:
    payload = DeactivatedTenant(id="1232321321", deactivated_date=utils.time_millis())
    event = TenantEvent(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        data_content_type=DeactivatedTenant.__name__,
        deactivated_tenant=payload,
    )
    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "tenant-events")
    return {"status": "ok"}


# Commands
@app.get("/test-register-tenant", include_in_schema=False)
async def test_register_tenant() -> dict[str, str]:
    payload = RegisterTenant(
        name="Camilo",
        last_name="Galvez",
        email="cgalvez@uniandes.edu.co",
        tenant_type=TenantType.natural,
        created_date=utils.time_millis(),
    )
    command = CommandRegisterTenant(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        data_content_type=RegisterTenant.__name__,
        data=payload,
    )
    dispatcher = Dispatcher()
    dispatcher.publish_message(command, "command-register-tenant")
    return {"status": "ok"}


@app.get("/test-validate-tenant", include_in_schema=False)
async def test_validate_tenant() -> dict[str, str]:
    payload = ValidateTenant(id="1232321321", validation_date=utils.time_millis())
    command = CommandValidateTenant(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        data_content_type=ValidateTenant.__name__,
        data=payload,
    )
    dispatcher = Dispatcher()
    dispatcher.publish_message(command, "command-validate-tenant")
    return {"status": "ok"}


@app.get("/test-deactivate-tenant", include_in_schema=False)
async def test_deactivate_tenant() -> dict[str, str]:
    payload = DeactivateTenant(id="1232321321", deactivated_date=utils.time_millis())
    command = CommandDeactivateTenant(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        data_content_type=DeactivateTenant.__name__,
        data=payload,
    )
    dispatcher = Dispatcher()
    dispatcher.publish_message(command, "command-deactivate-tenant")
    return {"status": "ok"}


@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(v1, prefix="/v1", tags=["Version 1"])
