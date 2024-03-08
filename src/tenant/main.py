from fastapi import FastAPI
from tenant.config.api import app_configs, settings
from tenant.api.v1.router import router as v1

from tenant.module.infrastructure.consumers import subscribe_to_topic
from tenant.module.infrastructure.v1.events import TenantEvent, ValidatedTenant, DeactivatedTenant, RegisteredTenant, TenantType
from tenant.module.infrastructure.v1.commands import CommandRegisterTenant, CommandValidateTenant, CommandDeactivateTenant, RegisterTenant, ValidateTenant, DeactivateTenant
from tenant.module.infrastructure.v1 import TenantType
from tenant.module.infrastructure.dispatchers import Dispatcher
from tenant.seedwork.infrastructure import utils

import asyncio
import time
import traceback
import uvicorn


app = FastAPI(**app_configs)
tasks = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(subscribe_to_topic("tenant-events", "sub-tenant", TenantEvent))
    task2 = asyncio.ensure_future(subscribe_to_topic("command-register-tenant", "sub-com-register-tenant", CommandRegisterTenant))
    task3 = asyncio.ensure_future(subscribe_to_topic("command-validate-tenant", "sub-com-validate-tenant", CommandValidateTenant))
    task4 = asyncio.ensure_future(subscribe_to_topic("command-deactivate-tenant", "sub-com-deactivate-tenant", CommandDeactivateTenant))
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)
    tasks.append(task4)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

#Events
@app.get("/test-validated-tenant", include_in_schema=False)
async def test_validated_tenant() -> dict[str, str]:
    payload = ValidatedTenant(id = "1232321321", validation_date = utils.time_millis())
    event = TenantEvent(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ValidatedTenant.__name__,
        validated_tenant = payload
    )
    distpacher = Dispatcher()
    distpacher.publish_message(event, "tenant-events")
    return {"status": "ok"}

@app.get("/test-registered-tenant", include_in_schema=False)
async def test_registered_tenant() -> dict[str, str]:
    payload = RegisteredTenant(
        id = "1232321321", 
        name = "Camilo",
        last_name = "Galvez",
        email = "cgalvez@uniandes.edu.co",
        tenant_type = TenantType.natural,
        created_date = utils.time_millis()
    )
    event = TenantEvent(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RegisteredTenant.__name__,
        registered_tenant = payload    
    )
    distpacher = Dispatcher()
    distpacher.publish_message(event, "tenant-events")
    return {"status": "ok"}

@app.get("/test-deactivated-tenant", include_in_schema=False)
async def test_deactivated_tenant() -> dict[str, str]:
    payload = DeactivatedTenant(
        id = "1232321321", 
        deactivated_date = utils.time_millis()
    )
    event = TenantEvent(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=DeactivatedTenant.__name__,
        deactivated_tenant = payload
    )
    distpacher = Dispatcher()
    distpacher.publish_message(event, "tenant-events")
    return {"status": "ok"}

#Commands
@app.get("/test-register-tenant", include_in_schema=False)
async def test_register_tenant() -> dict[str, str]:
    payload = RegisterTenant(
        name = "Camilo",
        last_name = "Galvez",
        email = "cgalvez@uniandes.edu.co",
        tenant_type = TenantType.natural,
        created_date = utils.time_millis()
    )
    command = CommandRegisterTenant(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RegisterTenant.__name__,
        data = payload
    )
    distpacher = Dispatcher()
    distpacher.publish_message(command, "command-register-tenant")
    return {"status": "ok"}

@app.get("/test-validate-tenant", include_in_schema=False)
async def test_validate_tenant() -> dict[str, str]:
    payload = ValidateTenant(
        id = "1232321321", 
        validation_date = utils.time_millis()
    )
    command = CommandValidateTenant(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ValidateTenant.__name__,
        data = payload
    )
    distpacher = Dispatcher()
    distpacher.publish_message(command, "command-validate-tenant")
    return {"status": "ok"}

@app.get("/test-deactivate-tenant", include_in_schema=False)
async def test_deactivate_tenant() -> dict[str, str]:
    payload = DeactivateTenant(
        id = "1232321321", 
        deactivated_date = utils.time_millis()
    )
    command = CommandDeactivateTenant(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=DeactivateTenant.__name__,
        data = payload
    )
    distpacher = Dispatcher()
    distpacher.publish_message(command, "command-deactivate-tenant")
    return {"status": "ok"}

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(v1, prefix="/v1", tags=["Version 1"])