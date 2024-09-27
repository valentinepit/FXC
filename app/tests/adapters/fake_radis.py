from app.adapters.redis import BaseRedisAdapter


class RedisAdapterMock(BaseRedisAdapter):
    def __init__(self):
        self.store = {}

    def connect(self):
        pass

    def disconnect(self):
        pass

    def get_by_key(self, key: str):
        return self.store.get(key, None)

    def send_by_key(self, key: str, value, ex=None):  # A003
        self.store[key] = value
