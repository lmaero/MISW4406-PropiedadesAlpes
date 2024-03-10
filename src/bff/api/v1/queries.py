import strawberry
from .schemas import *

@strawberry.type
class Query:
    transactions: typing.List[Transaction] = strawberry.field(resolve=get_transactions)