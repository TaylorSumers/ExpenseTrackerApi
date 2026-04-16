from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import ConflictError
from app.common.money import to_minor_units
from app.database import get_session_factory
from app.exceptions import NotFoundError
from app.models import Budget, Category


async def get_budgets(user_id: int, period: str) -> list[Budget]:
	async with get_session_factory() as session:
		budgets = await session.execute(select(Budget).filter_by(user_id=user_id, period=period))
		return budgets.scalars().all()


async def create_budget(user_id: int, category_id: int, period: str, limit: Decimal) -> None:
	budget = Budget(
		user_id=user_id,
		period=period,
		limit=to_minor_units(limit)
	)
	async with get_session_factory() as session:
		category = session.get(Category, category_id)
		if category is None or (not category.is_system and category.user_id != user_id):
			raise NotFoundError('Category not found')

		budget.category = category
		session.add(budget)
		try:
			await session.commit()
		except IntegrityError:
			await session.rollback()
			raise ConflictError('User already has a budget for such period with such category')
