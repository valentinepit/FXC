from abc import ABC, abstractmethod


class BaseConnector(ABC):

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def consumer(self):
        raise NotImplementedError

    @abstractmethod
    def producer(self, *args):
        raise NotImplementedError
