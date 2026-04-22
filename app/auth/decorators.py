from functools import wraps

from flask import g, request

from app.auth.tokens import decode_access_token
from app.database import get_session
from app.exceptions import UnauthorizedError
from app.models import User


def get_current_user() -> User:
	user = getattr(g, 'current_user', None)
	if not user:
		raise UnauthorizedError('Authentication required')
	return user


def auth_required(view):
	@wraps(view)
	async def wrapper(*args, **kwargs):
		auth_header = request.headers.get('Authorization', '')
		scheme, _, token = auth_header.partition(' ')

		if scheme.lower() != 'bearer' or not token:
			return UnauthorizedError('Missing or invalid Authorization header')

		payload = decode_access_token(token)
		user_id = int(payload['sub'])

		async with get_session() as session:
			user = await session.get(User, user_id)

		if user is None:
			raise UnauthorizedError('User from token was not found')

		g.current_user = user
		return await view(*args, **kwargs)

	return wrapper