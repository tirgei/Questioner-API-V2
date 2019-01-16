from abc import ABC, abstractmethod


class Model(ABC):
    """ Base model class for objects """

    def __init__(self):
        pass

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def exists(self, key, value):
        pass
