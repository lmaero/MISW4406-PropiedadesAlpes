import strawberry
import typing
from .schemas import get_transactions, Transaction

@strawberry.type
class Query:
    transactions: typing.List[Transaction] = strawberry.field(resolver=get_transactions)