from sqlalchemy.exc import IntegrityError

from app import ConflictError
from app.database import session_factory
from app.exceptions import NotFoundError
from app.models import Transaction


async def get_transaction(transaction_id: int) -> Transaction:
	async with session_factory() as session:
		transaction = await session.get(Transaction, transaction_id)
		return transaction


async def create_transaction(user_id, category_id, amount, type, description, executed_at) -> None:
	transaction = Transaction(
		user_id = user_id,
		category_id = category_id,
		amount = amount,
		type = type,
		description = description,
		executed_at = executed_at
	)

	async with session_factory() as session:
		session.add(transaction)
		await session.commit()


async def delete_transaction(transaction_id: int):
	async with session_factory() as session:
		transaction = await session.get(Transaction, transaction_id)

		if not transaction:
			raise NotFoundError('Transaction not found')

		session.delete(transaction)
		await session.commit()