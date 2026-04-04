from sqlalchemy import select

from app.database import session_factory
from app.models import User


async def register_user(username: str, email: str, password: str):
	password_hash = ''
	user = User(
		username=username,
		email=email,
		password_hash=password_hash
	)
	async with session_factory() as session:
		session.add(user)
		await session.commit()


async def login_user(email: str, password: str):
	async with session_factory() as session:
		password_hash = ''
		query = select(User).filter_by(email=email, password_hash=password_hash)
		result = await session.execute(query)
		return result.scalar()
