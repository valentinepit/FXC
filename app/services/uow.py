import abc

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings
from app.domain import HistoricalTransactions, InitialData
from app.repository.base import BaseRepository
from app.repository.historical_transactions import HistoricalTransactionsRepository
from app.repository.initial_data import InitialDataRepository


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def refresh_all(self, *args):
        for obj in args:
            self._refresh(obj)

    def refresh(self, obj):
        self._refresh(obj)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _refresh(self, obj):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractproperty
    def historical_transactions(self) -> BaseRepository:
        raise NotImplementedError

    @abc.abstractproperty
    def initial_data(self) -> BaseRepository:
        raise NotImplementedError


def get_engine(db_name):
    return create_engine(
        URL.create(
            'postgresql',
            username=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=db_name,
        )
    )


def get_session_factory(engine):
    return sessionmaker(autoflush=False, bind=engine, class_=Session)


sesion_factory = get_session_factory(engine=get_engine(db_name=settings.db_name))


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=sesion_factory):
        super().__init__()
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self._initial_data = InitialDataRepository(session=self.session, model_cls=InitialData)
        self._historical_transactions = HistoricalTransactionsRepository(
            session=self.session, model_cls=HistoricalTransactions
        )
        return super().__enter__()

    @property
    def initial_data(self) -> InitialDataRepository:
        return self._initial_data

    @property
    def historical_transactions(self) -> HistoricalTransactionsRepository:
        return self._historical_transactions

    def bulk_add(self, *args):
        self.session.add_all(*args)

    def __exit__(self, *args):
        self.session.expunge_all()
        super().__exit__(*args)
        # asyncio.shield(self.session.close())
        self.session = None

    def _commit(self):
        self.session.commit()

    def _refresh(self, obj):
        self.session.refresh(obj)

    def rollback(self):
        self.session.rollback()
