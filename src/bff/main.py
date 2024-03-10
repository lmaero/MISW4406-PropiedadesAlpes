from fastapi import FastAPI, Request
import asyncio
import time
import traceback
import uvicorn
import uuid
import datetime


from pydantic import BaseSettings
from typing import Any

from .consumidores import suscribirse_a_topico
from .despachadores import Despachador

from . import utils
from .api.v1.router import router as v1

from sse_starlette.sse import EventSourceResponse

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "BFF-Web PDA"}

app = FastAPI(**app_configs)
tasks = list()
eventos = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    global events
    task1 = asyncio.ensure_future(suscribirse_a_topico("transaction-event", "pda-bff", "public/default/transactions-event", events=events))
    tasks.append(task1)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get('/stream')
async def stream_messages(request: Request):
    def new_event():
        global events
        return {'data': eventos.pop(), 'event': 'NewEvent'}
    async def read_events():
        global events
        while True:
            # If client close the connection stop sending events
            if await request.is_disconnected():
                break

            if len(eventss) > 0:
                yield new_event()

            await asyncio.sleep(0.1)

    return EventSourceResponse(read_events())


app.include_router(v1, prefix="/v1")