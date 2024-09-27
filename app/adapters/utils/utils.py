from app.adapters.redis import RedisAdapter
from app.config import settings


def update_redis_value(key, value):
    redis_connector = RedisAdapter(host=settings.redis_host, port=settings.redis_port)
    redis_connector.connect()
    current_value = int(redis_connector.get_message_by_key(key))
    if not current_value:
        redis_connector.send_message_by_key(key, value)
    else:
        redis_connector.send_message_by_key(key, current_value + value)
