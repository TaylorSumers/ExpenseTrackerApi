from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import ConflictError
from app.database import get_session_factory
from app.models import Category


async def get_categories(user_id: int) -> list[Category]:
	async with get_session_factory() as session:
		result = await session.execute(select(Category).filter_by(user_id=user_id))
		return result.scalars().all()


async def create_category(user_id: int, name: str) -> None:
	category = Category(
		user_id=user_id,
		name=name
	)

	async with get_session_factory() as session:
		session.add(category)
		try:
			await session.commit()
		except IntegrityError:
			session.rollback()
			raise ConflictError('User already has a category with such name')
