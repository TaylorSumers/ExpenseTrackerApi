from http import HTTPStatus
from flask import Blueprint

from app.exceptions import BadRequestError
from app.responses import success_response
from app.schemas.categories import CreateCategoryRequest, GetCategoriesRequest, CategoryResponse
from app.services.category_service import get_categories, create_category
from app.validation import validate_body, validate_query

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.get('/get_categories')
async def get():
	payload = await validate_query(GetCategoriesRequest)
	categories = await get_categories(payload.user_id)
	response = [CategoryResponse(
		id=category.id,
		name=category.name,
		is_system=category.is_system,
		user_id=category.user_id
	).model_dump() for category in categories]
	return success_response(response)



@categories_bp.post('/create_category')
async def create():
	payload = validate_body(CreateCategoryRequest)
	await create_category(payload.user_id, payload.name)
	return success_response(status_code=HTTPStatus.CREATED)
