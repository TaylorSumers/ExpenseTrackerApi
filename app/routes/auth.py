from http import HTTPStatus
from flask import Blueprint, request

from app.exceptions import BadRequestError
from app.responses import success_response
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.post('/register')
async def register():
	data = request.get_json() or {}

	username = data.get("username")
	email = data.get("email")
	password = data.get("password")

	if not username or not email or not password:
		raise BadRequestError("username, email and password are required")

	user = await register_user(username, email, password)
	return success_response({'id': user.id}, status_code=HTTPStatus.CREATED)


@auth_bp.post('/login')
async def login():
	data = request.get_json() or {}

	email = data.get("email")
	password = data.get("password")

	if not email or not password:
		raise BadRequestError("email and password are required")

	user = await login_user(email, password)
	return success_response({'id': user.id})
