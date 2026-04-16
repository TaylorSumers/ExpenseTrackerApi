from http import HTTPStatus
from flask import Blueprint

from app.auth.decorators import get_current_user, auth_required
from app.responses import success_response
from app.schemas.categories import CreateCategoryRequest, CategoryResponse
from app.services.category_service import get_categories, create_category
from app.validation import validate_body

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.get('/get_categories')
@auth_required
async def get():
	current_user = get_current_user()
	categories = await get_categories(current_user.id)
	response = [CategoryResponse(
		id=category.id,
		name=category.name,
		is_system=category.is_system,
		user_id=category.user_id
	).model_dump() for category in categories]
	return success_response(response)



@categories_bp.post('/create_category')
@auth_required
async def create():
	current_user = get_current_user()
	payload = validate_body(CreateCategoryRequest)
	await create_category(current_user.id, payload.name)
	return success_response(status_code=HTTPStatus.CREATED)
