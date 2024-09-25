from abc import ABC, abstractmethod


class BaseConnector(ABC):
    @abstractmethod
    async def consumer(self):
        pass

    @abstractmethod
    async def producer(self, *args):
        pass
