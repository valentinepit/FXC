from app.config import settings
from app.connectors.redis import RedisConnector
from app.services.uow import SqlAlchemyUnitOfWork
from app.services import historical_transactions as historical_transactions_service


def on_message(channel, method_frame, header_frame, body):
    body_str = body.decode("utf-8")[:4000]
    uow = SqlAlchemyUnitOfWork()
    print(body_str)
    transaction = historical_transactions_service.create_transaction(uow, body_str)
    if not transaction:
        print('Wrong method')
    key, value = tuple(transaction.items())[0]
    update_redis_value(key, value)


def update_redis_value(key, value):
    redis_connector = RedisConnector(host=settings.redis_host, port=settings.redis_port)
    redis_connector.connect()
    current_value = int(redis_connector.consumer(key))
    if not current_value:
        redis_connector.producer(key, value)
    else:
        redis_connector.producer(key, current_value + value)
