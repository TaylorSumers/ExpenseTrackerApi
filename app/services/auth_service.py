from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import session_factory
from app.models import User


async def register_user(username: str, email: str, password: str):
	user = User(
		username=username,
		email=email,
		password_hash=generate_password_hash(password)
	)
	async with session_factory() as session:
		session.add(user)
		await session.commit()


async def login_user(email: str, password: str):
	async with session_factory() as session:
		query = select(User).filter_by(email=email)
		result = await session.execute(query)
		user = result.scalar_one_or_none()
		if not user or not check_password_hash(user.password_hash, password):
			raise Exception('Invalid credentials')
		return user.id
