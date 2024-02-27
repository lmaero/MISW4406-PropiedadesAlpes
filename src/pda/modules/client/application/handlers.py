from pda.seedwork.application.handlers import Handler


class DomainTransactionHandler(Handler):
    @staticmethod
    def create_transaction_handler():
        print("=========== TRANSACTION CREATED ===========")
