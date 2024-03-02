import logging
import traceback

from pydispatch import dispatcher

from pda.config.db import db
from pda.seedwork.infrastructure.uow import UnitOfWork, Batch


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnitOfWork:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _clean_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        return list[db.session.get_nested_transaction()]

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    def commit(self):
        for batch in self.batches:
            batch.operation(*batch.args, **batch.kwargs)

        db.session.commit()
        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()

        super().rollback()

    def savepoint(self):
        db.session.begin_nested()


class PulsarUnitOfWork(UnitOfWork):
    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnitOfWork:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _clean_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    def commit(self):
        index = 0
        try:
            for event in self._get_events():
                dispatcher.send(
                    signal=f"{type(event).__name__}Integration", event=event
                )
                index += 1
        except:
            logging.error("ERROR: Cannot subscribe to events topic!")
            traceback.print_exc()
            self.rollback(index=index)
        self._clean_batches()

    def rollback(self, index=None):
        super().rollback()

    def savepoint(self):
        pass
