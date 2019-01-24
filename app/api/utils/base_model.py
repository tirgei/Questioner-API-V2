from abc import ABC, abstractmethod
from db.db_config import DatabaseConnection


class Model(ABC, DatabaseConnection):
    """ Base model class for objects """

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def find(self, id):
        pass

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def exists(self, key, value):
        pass

    @abstractmethod
    def where(self, key, value):
        pass

    @abstractmethod
    def delete(self, id):
        pass
