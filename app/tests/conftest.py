import pytest
from sqlalchemy_utils import create_database, database_exists

from app.config import settings
from app.domain.models import Base
from app.services.uow import SqlAlchemyUnitOfWork, get_engine, get_session_factory
from app.tests.adapters.fake_rabbit import RabbitAdapterMock
from app.tests.adapters.fake_radis import RedisAdapterMock


def get_sqlalchemy_uow():
    engine = get_engine(db_name=f'test_{settings.db_name}')
    session_factory = get_session_factory(engine)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    return SqlAlchemyUnitOfWork(session_factory=session_factory)


@pytest.fixture
def sqlalchemy_uow():
    return get_sqlalchemy_uow()


@pytest.fixture
def fake_redis_adapter():
    return RedisAdapterMock()


@pytest.fixture
def fake_rabbit_adapter():
    return RabbitAdapterMock()
