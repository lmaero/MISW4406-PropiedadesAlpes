from pydispatch import dispatcher

from pda.modules.properties.domain.events import CreatedTransaction
from .handlers import TransactionIntegrationHandler

dispatcher.connect(
    TransactionIntegrationHandler.created_transaction_handler,
    signal=f"{CreatedTransaction.__name__}Integration",
)
