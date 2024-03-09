import asyncio
from typing import Any

from fastapi import FastAPI
from pydantic import BaseSettings

from . import utils
from .commands import (
    CommandPayTransaction,
    CommandReversePayment,
    PayTransactionPayload,
    ReversePaymentPayload,
)
from .consumers import subscribe_to_topic
from .dispatchers import Dispatcher
from .events import EventPayment, PaidTransaction, ReversedPayment


class Config(BaseSettings):
    APP_VERSION: str = "1"


settings = Config()
app_configs: dict[str, Any] = {"title": "Payments PDA"}

app = FastAPI(**app_configs)
tasks = list()


@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(
        subscribe_to_topic("payment-events", "sub-payments", EventPayment)
    )
    task2 = asyncio.ensure_future(
        subscribe_to_topic(
            "command-pay-transaction", "sub-com-pay-transaction", CommandPayTransaction
        )
    )
    task3 = asyncio.ensure_future(
        subscribe_to_topic(
            "command-reverse-payments",
            "sub-com-reverse-payments",
            CommandReversePayment,
        )
    )
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)


@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()


# Events
@app.get("/test-paid-transaction", include_in_schema=False)
async def test_paid_transaction() -> dict[str, str]:
    payload = PaidTransaction(
        id="1232321321",
        correlation_id="389822434",
        transaction_id="6463454",
        amount=23412.12,
        amount_vat=234.0,
        creation_date=utils.time_millis(),
    )

    event = EventPayment(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=PaidTransaction.__name__,
        paid_transaction=payload,
    )

    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "payment-events")
    return {"status": "ok"}


@app.get("/test-reversed-payment", include_in_schema=False)
async def test_reversed_payment() -> dict[str, str]:
    payload = ReversedPayment(
        id="1232321321",
        correlation_id="389822434",
        transaction_id="6463454",
        update_date=utils.time_millis(),
    )

    event = EventPayment(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ReversedPayment.__name__,
        reversed_payment=payload,
    )

    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "payment-events")
    return {"status": "ok"}


# Commands
@app.get("/test-pay-transaction", include_in_schema=False)
async def test_pay_transaction() -> dict[str, str]:
    payload = PayTransactionPayload(
        correlation_id="389822434",
        transaction_id="6463454",
        amount=23412.12,
        amount_vat=234.0,
        creation_date=utils.time_millis(),
    )

    command = CommandPayTransaction(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=PayTransactionPayload.__name__,
        data=payload,
    )

    dispatcher = Dispatcher()
    dispatcher.publish_message(command, "command-pay-transaction")
    return {"status": "ok"}


@app.get("/test-reverse-payment", include_in_schema=False)
async def test_reverse_payment() -> dict[str, str]:
    payload = ReversePaymentPayload(
        id="1232321321", correlation_id="389822434", transaction_id="6463454"
    )

    command = CommandReversePayment(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ReversePaymentPayload.__name__,
        data=payload,
    )

    dispatcher = Dispatcher()
    dispatcher.publish_message(command, "command-reverse-payments")
    return {"status": "ok"}
