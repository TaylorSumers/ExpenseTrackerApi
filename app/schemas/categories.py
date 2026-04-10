from app.schemas.base import RequestSchema, ResponseSchema
from pydantic import Field


class GetCategoriesRequest(RequestSchema):
	user_id: int


class CreateCategoryRequest(RequestSchema):
	user_id: int
	name: str = Field(min_length=1, max_length=100)


class CategoryResponse(ResponseSchema):
	id: int
	name: str
	is_system: bool
	user_id: int