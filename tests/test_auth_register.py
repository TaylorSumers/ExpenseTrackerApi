import asyncio

from sqlalchemy import select

from app.database import get_session
from app.models import User
from app.schemas.auth import RegisterRequest

register_request = RegisterRequest(
	username='test',
	email='test@mail.ru',
	password='passpass'
)


def test_auth_register_success_response(client):
	response = client.post('/auth/register', json=register_request.model_dump())

	assert response.status_code == 201
	assert response.get_json()['data']['token_type'] == 'Bearer'


def test_auth_register_creates_user_in_db(client):
	response = client.post('/auth/register', json=register_request.model_dump())

	assert response.status_code == 201

	async def get_created_user():
		async with get_session() as session:
			result = await session.execute(select(User).filter_by(email=register_request.email))
			return result.scalar_one_or_none()

	user = asyncio.run(get_created_user())
	assert user is not None
	assert user.username == register_request.username
	assert user.email == register_request.email
