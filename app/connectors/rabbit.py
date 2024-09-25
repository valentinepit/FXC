import pika

from app.config import settings
from app.connectors.utils.utils import on_message


class RabbitConnector:
    def __init__(self, host, port, user, password):
        self.password = password
        self.user = user
        self.port = port
        self.host = host
        self.connection, self.credentials, self.rmq_channel, self.rmq_connection = None, None, None, None
        # super().__init__()

    def connect(self):
        # TODO need to try and reconnect in case of error
        self.credentials = pika.PlainCredentials(self.user, self.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port,
                                      credentials=self.credentials))
        self.rmq_channel = self.connection.channel()

    def disconnect(self):
        self.rmq_connection.close()

    def consumer(self):
        self.rmq_channel.basic_consume(settings.queue_name, on_message)
        try:
            self.rmq_channel.start_consuming()
        except KeyboardInterrupt:
            self.rmq_channel.stop_consuming()
        except Exception:
            self.rmq_channel.stop_consuming()

    def producer(self, *args):
        pass
