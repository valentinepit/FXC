import json

from app.adapters.utils.utils import update_redis_value
from app.domain import InitialData
from app.services import historical_transactions as historical_transaction_service
from app.services.uow import SqlAlchemyUnitOfWork
from app.tests.adapters.fake_rabbit import RabbitAdapterMock
from app.tests.adapters.fake_radis import RedisAdapterMock


def test_create_transaction_success(
    sqlalchemy_uow: SqlAlchemyUnitOfWork,
    fake_redis_adapter: RedisAdapterMock,
    fake_rabbit_adapter: RabbitAdapterMock,
):
    new_data = fake_rabbit_adapter.consumer()
    new_data_dict = json.loads(new_data)
    with sqlalchemy_uow as uow:
        uow.initial_data.add(
            InitialData(id=new_data_dict['id'], provider_name='Visa', initial_value=new_data_dict['value'])
        )
        uow.commit()

    transaction = historical_transaction_service.create_transaction(sqlalchemy_uow, new_data)

    assert transaction.transaction_value == new_data_dict['value']


def test_create_transaction_fail(
    sqlalchemy_uow: SqlAlchemyUnitOfWork,
    fake_redis_adapter: RedisAdapterMock,
    fake_rabbit_adapter: RabbitAdapterMock,
):
    new_data = fake_rabbit_adapter.consumer()
    new_data_dict = json.loads(new_data)
    with sqlalchemy_uow as uow:
        uow.initial_data.add(
            InitialData(id=new_data_dict['id'], provider_name='Visa', initial_value=new_data_dict['value'])
        )
        uow.commit()

    while new_data_dict['id'] == json.loads(new_data)['id']:
        new_data = fake_rabbit_adapter.consumer()

    transaction = historical_transaction_service.create_transaction(sqlalchemy_uow, new_data)
    assert transaction is None


def test_update_redis_value(fake_redis_adapter: RedisAdapterMock):
    update_redis_value('test_key', 1, fake_redis_adapter)
    update_redis_value('test_key', 2, fake_redis_adapter)
    update_redis_value('test_key_2', 1, fake_redis_adapter)
    assert fake_redis_adapter.get_by_key('test_key') == 3
    assert fake_redis_adapter.get_by_key('test_key_2') == 1
