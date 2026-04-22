from decimal import Decimal
from datetime import datetime

from sqlalchemy import select

from app.common.money import to_minor_units
from app.database import get_session
from app.exceptions import NotFoundError
from app.models import Transaction, Category


async def get_transaction(transaction_id: int, user_id: int) -> Transaction:
	async with get_session() as session:
		transaction = await session.execute(select(Transaction).filter_by(id=transaction_id, user_id=user_id))

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
		amount=to_minor_units(amount),
		type=type,
		description=description,
		executed_at=executed_at
	)

	async with get_session() as session:
		category = await session.get(Category, category_id)
		if category is None or (not category.is_system and category.user_id != user_id):
			raise NotFoundError('Category not found')

		session.add(transaction)
		await session.commit()


async def delete_transaction(transaction_id: int, user_id: int):
	async with get_session() as session:
		transaction = await session.execute(select(Transaction).filter_by(id=transaction_id, user_id=user_id))

		if not transaction:
			raise NotFoundError('Transaction not found')

		await session.delete(transaction)
		await session.commit()
