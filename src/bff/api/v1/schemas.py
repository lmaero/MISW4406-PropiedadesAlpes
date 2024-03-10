import typing
import strawberry
import uuid
import requests
import os

from datetime import datetime


PDA_HOST = os.getenv("PDA_ADDRESS", default="localhost")
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def get_transactions(root) -> typing.List["Transaction"]:
    transactions_json = requests.get(f'http://{PDA_HOST}:5000/properties/transaction').json()
    transactions = []

    for transaction in transactions_json:
        transactions.append(
            Transaction(
                creation_date=datetime.strptime(transaction.get('creation_date'), DATE_FORMAT),
                update_date=datetime.strptime(transaction.get('update_date'), DATE_FORMAT),
                id=transaction.get('id'),
                id_usuario=transaction.get('id_user', '')
            )
        )

    return transactions

@strawberry.type
class Leasing:
    # TODO Completar objeto strawberry para incluir los itinerarios
    ...

@strawberry.type
class Transaction:
    id: str
    id_user: str
    creation_date: datetime
    update_date: datetime
    #itinerarios: typing.List[Itinerario]

@strawberry.type
class TransactionAnswer:
    message: str
    code: int