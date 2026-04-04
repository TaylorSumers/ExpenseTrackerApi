from sqlalchemy import select

from app.database import session_factory
from app.models import Budget


async def get_budgets(user_id: int, period: str):
	async with session_factory() as session:
		query = select(Budget).filter_by(user_id=user_id, period=period)
		result = await session.execute(query)
		return result.scalars().all()


async def create_budget(user_id: int, category_id: int, period: str, limit: int):
	budget = Budget(
		user_id=user_id,
		category_id=category_id,
		period=period,
		limit=limit
	)
	async with session_factory() as session:
		session.add(budget)
		await session.commit()