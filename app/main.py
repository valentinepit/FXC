from connectors.rabbit import RabbitConnector
from config import settings

if __name__ == '__main__':
    rmq_conn = RabbitConnector(host=settings.rabbitmq_host, port=settings.rabbitmq_port, user=settings.rabbitmq_user,
                               password=settings.rabbitmq_password)
    rmq_conn.connect()
    rmq_conn.consumer()
