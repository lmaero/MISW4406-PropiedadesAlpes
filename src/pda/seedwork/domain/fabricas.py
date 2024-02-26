from abc import ABC, abstractmethod

from .mixins import ValidateMixinRules
from .repositorios import Mapper


class Factory(ABC, ValidateMixinRules):
    @abstractmethod
    def create_object(self, obj: any, mapper: Mapper = None) -> any:
        pass
