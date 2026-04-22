from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import ConflictError
from app.database import get_session
from app.models import Category


async def get_categories(user_id: int) -> Sequence[Category]:
	async with get_session() as session:
		result = await session.execute(select(Category).filter_by(user_id=user_id))
		return result.scalars().all()


async def create_category(user_id: int, name: str) -> None:
	category = Category(
		user_id=user_id,
		name=name
	)

	async with get_session() as session:
		session.add(category)
		try:
			await session.commit()
		except IntegrityError:
			await session.rollback()
			raise ConflictError('User already has a category with such name')
