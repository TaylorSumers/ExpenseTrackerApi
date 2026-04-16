from pydantic import Field
from decimal import Decimal

from app.schemas.base import RequestSchema, ResponseSchema


class GetBudgetsRequest(RequestSchema):
	period: str = Field(min_length=7, max_length=7, pattern=r"^\d{4}-\d{2}$")


class CreateBudgetRequest(RequestSchema):
	category_id: int
	period: str = Field(min_length=7, max_length=7, pattern=r"^\d{4}-\d{2}$")
	limit: Decimal = Field(gt = 0)


class BudgetResponse(ResponseSchema):
	id: int
	category: str
	period: str
	limit: Decimal
