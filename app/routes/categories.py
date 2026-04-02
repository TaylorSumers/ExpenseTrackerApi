from flask import Blueprint, request
from app.services.category_service import get_categories, create_category

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.get('/get_categories')
def get():
	data = request.get_json() or {}
	user_id = data.get("user_id")
	if not user_id:
		return {"message": "user_id is required"}, 400
	result = get_categories(user_id)
	return result, 200



@categories_bp.post('/create_category')
def create():
	data = request.get_json() or {}
	user_id = data.get("user_id")
	name = data.get("name")
	if not user_id or not name:
		return {"message": "user_id and name are required"}, 400
	result = create(user_id, name)
	return result, 201
