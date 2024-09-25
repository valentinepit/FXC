import json
from app.domain import HistoricalTransactions
from app.services.uow import SqlAlchemyUnitOfWork


def create_transaction(uow: SqlAlchemyUnitOfWork, data: str) -> dict | None:
    transaction_data = json.loads(data)
    with uow:
        method = uow.initial_data.get('id', transaction_data['id'])
        if not method:
            return None
        transaction = HistoricalTransactions(provider_id=transaction_data['id'],
                                             transaction_value=transaction_data['value'])
        uow.historical_transactions.add(transaction)
        uow.commit()
        uow.refresh(transaction)
        print(
            f'Created transaction {transaction.id} for {transaction.initial_data.provider_name} with value {transaction.transaction_value}')
        tr_dict = {f'{transaction.initial_data.id}_{transaction.initial_data.provider_name}': int(transaction.transaction_value)}
        return tr_dict
