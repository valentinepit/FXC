from app.adapters.redis import BaseRedisAdapter


def update_redis_value(key, value, adapter: BaseRedisAdapter):
    adapter.connect()
    current_value = adapter.get_by_key(key)
    if not current_value:
        adapter.send_by_key(key, value)
    else:
        adapter.send_by_key(key, int(current_value) + value)
