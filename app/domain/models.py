from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003


class InitialData(Base):
    __tablename__ = "initial_data"

    provider_name: Mapped[str]
    initial_value: Mapped[int]
    historical_transactions: Mapped[list['HistoricalTransactions'] | None] = relationship(back_populates='initial_data',
                                                                                          cascade='all, delete-orphan')


class HistoricalTransactions(Base):
    __tablename__ = "historical_transactions"

    transaction_value: Mapped[int]

    provider_id: Mapped[int] = mapped_column(ForeignKey('initial_data.id'))
    initial_data: Mapped['InitialData'] = relationship(back_populates='historical_transactions')
