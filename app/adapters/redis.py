import redis


class RedisAdapter:
    def __init__(self, host, port, user=None, password=None):
        self.password = password
        self.user = user
        self.port = port
        self.host = host
        self.redis_connection = None

    def connect(self):
        self.redis_connection = redis.Redis(decode_responses=True)

    def disconnect(self):
        self.redis_connection.close()

    def get_message_by_key(self, key: str) -> int | None:
        return self.redis_connection.get(key)

    def send_message_by_key(self, key: str, value: int) -> None:
        self.redis_connection.set(key, value)
