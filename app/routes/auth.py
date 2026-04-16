from http import HTTPStatus
from flask import Blueprint

from app.auth.tokens import create_access_token
from app.responses import success_response
from app.schemas.auth import RegisterRequest, TokenResponse, LoginRequest
from app.services.auth_service import register_user, login_user
from app.validation import validate_body

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.post('/register')
async def register():
	payload = validate_body(RegisterRequest)
	user = await register_user(payload.username, payload.email, payload.password)
	token = create_access_token(user.id)
	response = TokenResponse(access_token=token)
	return success_response(response.model_dump(), status_code=HTTPStatus.CREATED)


@auth_bp.post('/login')
async def login():
	payload = validate_body(LoginRequest)
	user = await login_user(payload.email, payload.password)
	token = create_access_token(user.id)
	response = TokenResponse(access_token=token)
	return success_response(response.model_dump())
