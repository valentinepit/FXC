import pika

from app.adapters.redis import RedisAdapter
from app.adapters.utils.utils import update_redis_value
from app.config import logger, settings
from app.services import historical_transactions as historical_transactions_service
from app.services.uow import SqlAlchemyUnitOfWork


class RabbitAdapter:
    def __init__(self, host, port, user, password):
        self.password = password
        self.user = user
        self.port = port
        self.host = host
        self.connection, self.credentials, self.rmq_channel, self.rmq_connection = None, None, None, None

    def connect(self):
        self.credentials = pika.PlainCredentials(self.user, self.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials)
        )
        self.rmq_channel = self.connection.channel()

    def disconnect(self):
        self.rmq_connection.close()

    def consumer(self):
        self.rmq_channel.basic_consume(settings.queue_name, self.on_message)
        try:
            self.rmq_channel.start_consuming()
        except KeyboardInterrupt:
            self.rmq_channel.stop_consuming()
        except Exception:  # noqa PIE786
            self.rmq_channel.stop_consuming()

    @staticmethod
    def on_message(channel, method_frame, header_frame, body):
        body_str = body.decode('utf-8')[:4000]
        uow = SqlAlchemyUnitOfWork()
        logger.info(body_str)
        transaction = historical_transactions_service.create_transaction(uow, body_str)
        if not transaction:
            logger.info('Wrong method')
        redis_adapter = RedisAdapter(host=settings.redis_host, port=settings.redis_port)
        update_redis_value(
            f'{transaction.initial_data.id}_{transaction.initial_data.provider_name}',
            int(transaction.transaction_value),
            adapter=redis_adapter,
        )
