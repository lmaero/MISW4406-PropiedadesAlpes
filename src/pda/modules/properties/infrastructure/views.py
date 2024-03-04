from pda.config.db import db
from pda.modules.properties.domain.entities import Transaction
from pda.seedwork.infrastructure.views import View
from .dto import Transaction as TransactionDTO


class TransactionView(View):
    def get_by(self, id_transaction=None, id_client=None, **kwargs) -> [Transaction]:
        params = dict()

        if id_transaction:
            params["id"] = str(id_transaction)

        if id_client:
            params["id"] = str(id_client)

        return db.session.query(TransactionDTO).filter_by(**params)
