from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import ConflictError
from app.database import get_session_factory
from app.models import Budget


async def get_budgets(user_id: int, period: str) -> list[Budget]:
	async with get_session_factory() as session:
		budgets = await session.execute(select(Budget).filter_by(user_id=user_id, period=period))
		return budgets.scalars().all()


async def create_budget(user_id: int, category_id: int, period: str, limit: int) -> None:
	budget = Budget(
		user_id=user_id,
		category_id=category_id,
		period=period,
		limit=limit
	)
	async with get_session_factory() as session:
		session.add(budget)
		try:
			await session.commit()
		except IntegrityError:
			await session.rollback()
			raise ConflictError('User already has a budget for such period with such category')
