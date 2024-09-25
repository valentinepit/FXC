from abc import ABC, abstractmethod


class BaseConnector(ABC):
    def __init__(self):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc, tb):
        pass

    @abstractmethod
    async def consumer(self):
        pass

    @abstractmethod
    async def producer(self, *args):
        pass