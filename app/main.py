from adapters.rabbit import RabbitAdapter
from config import settings

if __name__ == '__main__':
    rmq_conn = RabbitAdapter(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        user=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )
    rmq_conn.connect()
    rmq_conn.consumer()
