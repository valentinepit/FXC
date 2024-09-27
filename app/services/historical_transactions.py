import json

from app.config import logger
from app.domain import HistoricalTransactions
from app.services.uow import SqlAlchemyUnitOfWork


def create_transaction(uow: SqlAlchemyUnitOfWork, data: str) -> HistoricalTransactions | None:
    transaction_data = json.loads(data)
    with uow:
        provider_name = uow.initial_data.get('id', transaction_data['id'])
        if not provider_name:
            return None
        transaction = HistoricalTransactions(
            provider_id=transaction_data['id'], transaction_value=transaction_data['value']
        )
        uow.historical_transactions.add(transaction)
        uow.commit()
        uow.refresh(transaction)
        logger.info(
            f'Created transaction {transaction.id} for {transaction.initial_data.provider_name} '
            f'with value {transaction.transaction_value}'
        )
        return transaction
