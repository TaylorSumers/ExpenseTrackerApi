from sqlalchemy import select

from app.database import session_factory
from app.models import Category


async def get_categories(user_id: int):
	async with session_factory() as session:
		query = select(Category).filter_by(user_id=user_id)
		result = await session.execute(query)
		return result.scalars().all()

async def create_category(user_id: int, name: str):
	category = Category(
		user_id=user_id,
		name=name
	)
	async with session_factory() as session:
		session.add(category)
		await session.commit()