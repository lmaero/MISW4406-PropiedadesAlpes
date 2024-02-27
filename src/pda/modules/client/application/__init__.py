from pydispatch import dispatcher

from .handlers import DomainTransactionHandler

dispatcher.connect(
    DomainTransactionHandler.create_transaction_handler,
    signal="DomainCreatedTransaction",
)
