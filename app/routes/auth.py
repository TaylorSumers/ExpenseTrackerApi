from flask import Blueprint, request
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/register')
def register():
	data = request.get_json() or {}

	username = data.get("username") # TODO: создавать класс CreateUserCommand?
	email = data.get("email")
	password = data.get("password")

	if not username or not email or not password:
		return {"message": "username, email and password are required"}, 400

	result = register_user(username, email, password)

	return result, 201

@auth_bp.post('/login')
def login():

	data = request.get_json() or {}
	email = data.get("email")
	password = data.get("password")

	if not email or not password:
		return {"message": "email and password are required"}, 400

	result = login_user(email, password)
	return result, 200
