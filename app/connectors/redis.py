from app.config import settings
from app.connectors.base import BaseConnector
import redis

from app.services.uow import SqlAlchemyUnitOfWork
from app.services import historical_transactions as historical_transactions_service


class RedisConnector:
    def __init__(self, host, port, user=None, password=None):
        self.password = password
        self.user = user
        self.port = port
        self.host = host
        self.redis_connection = None
        # super().__init__()

    def connect(self):
        # TODO need to try and reconnect in case of error
        self.redis_connection = redis.Redis(decode_responses=True)

    def disconnect(self):
        self.redis_connection.close()

    def consumer(self, key: str) -> int | None:
        return self.redis_connection.get(key)

    def producer(self, key: str, value: int) -> None:
        self.redis_connection.set(key, value)
