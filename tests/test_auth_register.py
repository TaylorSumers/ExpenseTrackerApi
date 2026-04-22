import asyncio

from sqlalchemy import select

from app.database import get_session
from app.models import User

test_username = 'test'
test_email = 'test@mail.ru'
test_password = 'passpass'


def test_auth_register_success_response(client):
	response = client.post(
		'/auth/register',
		json={
			'username': test_username,
			'email': test_email,
			'password': test_password
		})
	assert response.status_code == 201
	assert response.get_json()['data']['token_type'] == 'Bearer'


def test_auth_register_creates_user_in_db(client):
	response = client.post(
		'/auth/register',
		json={
			'username': test_username,
			'email': test_email,
			'password': test_password
		})
	assert response.status_code == 201

	async def get_created_user():
		async with get_session() as session:
			result = await session.execute(select(User).filter_by(email=test_email))
			return result.scalar_one_or_none()

	user = asyncio.run(get_created_user())
	assert user is not None
	assert user.username == test_username
	assert user.email == test_email
