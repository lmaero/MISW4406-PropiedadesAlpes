from pda.modules.properties.infrastructure.dispatchers import Dispatcher
from pda.seedwork.application.handlers import Handler


class TransactionIntegrationHandler(Handler):
    @staticmethod
    def created_transaction_handler(event):
        dispatcher = Dispatcher()
        dispatcher.publish_event(event, "transaction-events")
