from pda.config.db import db
from pda.modules.properties.domain.entities import Transaction
from pda.seedwork.infrastructure.views import View
from .dto import Transaction as TransactionDTO


# TODO: Adapt to our schema
class TransactionView(View):
    def get_by(id=None, id_client=None, **kwargs) -> [Transaction]:
        params = dict()

        if id:
            params["id"] = str(id)

        if id_client:
            params["id_cliente"] = str(id_client)

        # TODO Convierta ReservaDTO a Reserva y valide que la consulta es correcta
        return db.session.query(TransactionDTO).filter_by(**params)
