from fastapi import FastAPI, Request
import asyncio
import traceback
import requests
import json


from pydantic import BaseSettings
from typing import Any

from .consumers import suscribe_to_topic
from .dispatchers import Dispatcher

from . import utils
from .api.v1.router import router as v1

from sse_starlette.sse import EventSourceResponse

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "BFF-Web PDA"}

app = FastAPI(**app_configs)
tasks = list()
events = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    global events
    task1 = asyncio.ensure_future(suscribe_to_topic("transaction-event", "pda-bff", "public/default/transaction-events", events=events))
    tasks.append(task1)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.post('/v1/properties/transaction')
async def create_transaction(request: Request):
    try:
        transaction_data = await request.json()
        response_json = requests.post(f'http://{utils.pda_host()}:{utils.pda_port()}/properties/transactions', json=transaction_data)
        if response_json.status_code != 202:
            return {"status": "error", "message": "An error occurred while creating the transaction"}
        return {"status": "success", "message": "Transaction created successfully"}
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": "An error occurred while creating the transaction"}


