import asyncio

from werkzeug.security import generate_password_hash

from app.database import get_session
from app.models import User
from app.schemas.auth import LoginRequest

login_request = LoginRequest(
	email='test@mail.ru',
	password='passpass'
)

async def register_test_user():
	user = User(
		username='test_username',
		email=login_request.email,
		password_hash=generate_password_hash(login_request.password)
	)
	async with get_session() as session:
		session.add(user)
		await session.commit()

def test_auth_login_success_response(client):
	asyncio.run(register_test_user())

	response = client.post('/auth/login', json=login_request.model_dump())

	assert response.status_code == 200
	assert response.get_json()['data']['token_type'] == 'Bearer'