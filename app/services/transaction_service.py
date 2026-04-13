from decimal import Decimal
from datetime import datetime

from app.common.money import to_minor_units
from app.database import get_session_factory
from app.exceptions import NotFoundError
from app.models import Transaction


async def get_transaction(transaction_id: int) -> Transaction:
	async with get_session_factory() as session:
		transaction = await session.get(Transaction, transaction_id)

		if not transaction:
			raise NotFoundError('Transaction not found')

		return transaction


async def create_transaction(
		user_id: id,
		category_id: int,
		amount: Decimal,
		type: str,
		description: str,
		executed_at: datetime
) -> None:
	transaction = Transaction(
		user_id=user_id,
		category_id=category_id,
		amount=to_minor_units(amount),
		type=type,
		description=description,
		executed_at=executed_at
	)

	async with get_session_factory() as session:
		session.add(transaction)
		await session.commit()


async def delete_transaction(transaction_id: int):
	async with get_session_factory() as session:
		transaction = await session.get(Transaction, transaction_id)

		if not transaction:
			raise NotFoundError('Transaction not found')

		session.delete(transaction)
		await session.commit()
