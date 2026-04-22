from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions import ConflictError, UnauthorizedError
from app.database import get_session
from app.models import User


async def register_user(username: str, email: str, password: str) -> User:
	user = User(
		username=username,
		email=email,
		password_hash=generate_password_hash(password)
	)

	async with get_session() as session:
		session.add(user)
		try:
			await session.commit()
		except IntegrityError:
			await session.rollback()
			raise ConflictError('Username or email already exists')

		await session.refresh(user)
		return user

async def login_user(email: str, password: str) -> User:
	async with get_session() as session:
		result = await session.execute(select(User).filter_by(email=email))
		user = result.scalar_one_or_none()

		if not user or not check_password_hash(user.password_hash, password):
			raise UnauthorizedError('Invalid credentials')

		return user
