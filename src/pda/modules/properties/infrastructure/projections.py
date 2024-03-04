import logging
import traceback
from abc import ABC, abstractmethod

from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.infrastructure.factories import RepositoryFactory
from pda.modules.properties.infrastructure.repositories import \
    TransactionsRepository
from pda.seedwork.infrastructure.projections import Projection, \
    ProjectionHandler
from pda.seedwork.infrastructure.projections import \
    execute_projection as projection
from pda.seedwork.infrastructure.utils import millis_a_datetime
from .dto import TransactionAnalytics


class TransactionProjection(Projection, ABC):
    @abstractmethod
    def execute(self): ...


class TotalTransactionsProjection(TransactionProjection):
    ADD = 1
    DELETE = 2
    UPDATE = 3

    def __init__(self, created_at, operation):
        self.created_at = millis_a_datetime(created_at)
        self.operation = operation

    def execute(self, db=None):
        if not db:
            logging.error("ERROR: application DB cannot be null")
            return
        record = (
            db.session.query(TransactionAnalytics)
            .filter_by(created_at=self.created_at.date())
            .one_or_none()
        )

        if record and self.operation == self.ADD:
            record.total += 1
        elif record and self.operation == self.DELETE:
            record.total -= 1
            record.total = max(record.total, 0)
        else:
            db.session.add(
                TransactionAnalytics(created_at=self.created_at.date(), total=1)
            )

        db.session.commit()


class TransactionsListProjection(TransactionProjection):
    def __init__(self, id_transaction, id_client, created_at, updated_at):
        self.id_transaction = id
        self.id_client = id_client
        self.created_at = millis_a_datetime(created_at)
        self.updated_at = millis_a_datetime(updated_at)

    def execute(self, db=None):
        if not db:
            logging.error("ERROR: application DB cannot be null")
            return

        repository_factory = RepositoryFactory()
        repository = repository_factory.create_object(TransactionsRepository)

        repository.add(
            Transaction(
                id=str(self.id_transaction),
                id_client=str(self.id_client),
                created_at=self.created_at,
                updated_at=self.updated_at,
            )
        )

        db.session.commit()


class TransactionProjectionHandler(ProjectionHandler):
    def handle(self, projection: TransactionProjection):
        from pda.config.db import db

        projection.execute(db=db)


@projection.register(TransactionsListProjection)
@projection.register(TotalTransactionsProjection)
def execute_transaction_projection(projection, app=None):
    if not app:
        logging.error("ERROR: application context cannot be null")
        return
    try:
        with app.app_context():
            handler = TransactionProjectionHandler()
            handler.handle(projection)

    except:
        traceback.print_exc()
        logging.error("ERROR: Persisting!")
