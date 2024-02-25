from abc import ABC, abstractmethod
from enum import Enum
from pda.seedwork.domain.entities import RootAggregation
from pydispatch import dispatcher

import pickle


class Lock(Enum):
    OPTIMIST = 1
    PESIMIST = 2


class Batch:
    def __init__(self, operation, lock: Lock, *args, **kwargs):
        self.operation = operation
        self.args = args
        self.lock = lock
        self.kwargs = kwargs


class UnitOfWork(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _get_events(self, batches=None):
        batches = self.batches if batches is None else batches
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, RootAggregation):
                    return arg.eventos
        return list()

    @abstractmethod
    def _clean_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError

    def commit(self):
        self._publish_events_post_commit()
        self._clean_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._clean_batches()

    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def register_batch(self, operation, *args, lock=Lock.PESIMIST, **kwargs):
        batch = Batch(operation, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publish_domain_events(batch)

    def _publish_domain_events(self, batch):
        for event in self._get_events(batches=[batch]):
            dispatcher.send(signal=f'{type(event).__name__}Dominio', event=event)

    def _publish_events_post_commit(self):
        for event in self._get_events():
            dispatcher.send(signal=f'{type(event).__name__}Integracion', event=event)


def is_flask():
    try:
        from flask import session
        return True
    except Exception as e:
        return False


def register_unit_of_work(serialized_obj):
    from pda.config.uow import UnitOfWorkSQLAlchemy
    from flask import session

    session['uow'] = serialized_obj


def flask_uow():
    from flask import session
    from pda.config.uow import UnitOfWorkSQLAlchemy
    if session.get('uow'):
        return session['uow']
    else:
        uow_serialized = pickle.dumps(UnitOfWorkSQLAlchemy())
        register_unit_of_work(uow_serialized)
        return uow_serialized


def unit_of_work() -> UnitOfWork:
    if is_flask():
        return pickle.loads(flask_uow())
    else:
        raise Exception('No hay unidad de trabajo')


def save_unit_of_work(uow: UnitOfWork):
    if is_flask():
        register_unit_of_work(pickle.dumps(uow))
    else:
        raise Exception('No hay unidad de trabajo')


class UnidadTrabajoPuerto:

    @staticmethod
    def commit():
        uow = unit_of_work()
        uow.commit()
        save_unit_of_work(uow)

    @staticmethod
    def rollback(savepoint=None):
        uow = unit_of_work()
        uow.rollback(savepoint=savepoint)
        save_unit_of_work(uow)

    @staticmethod
    def savepoint():
        uow = unit_of_work()
        uow.savepoint()
        save_unit_of_work(uow)

    @staticmethod
    def dar_savepoints():
        uow = unit_of_work()
        return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMIST, **kwargs):
        uow = unit_of_work()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)
        save_unit_of_work(uow)