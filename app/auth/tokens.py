from datetime import datetime, timezone, timedelta

import jwt

from app import settings
from app.exceptions import UnauthorizedError


def create_access_token(user_id: int) -> str:
	now = datetime.now(timezone.utc)
	payload = {
		'sub': str(user_id),
		'type': 'access',
		'iat': now,
		'exp': now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES)
	}
	return jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
	try:
		payload = jwt.decode(
			token,
			settings.JWT_SECRET_KEY,
			algorithms=[settings.JWT_ALGORITHM]
		)
	except jwt.ExpiredSignatureError as ex:
		raise UnauthorizedError('Access token expired') from ex
	except jwt.InvalidTokenError as ex:
		raise UnauthorizedError('Invalid access token') from ex

	if payload.get('type') != 'access':
		raise UnauthorizedError('Invalid token type')

	return payload