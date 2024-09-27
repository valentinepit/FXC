import json
import random


class RabbitAdapterMock:  # noqa PIE798
    @staticmethod
    def consumer():
        return json.dumps({'id': random.randint(1, 3), 'value': random.randint(-100, 100)})
