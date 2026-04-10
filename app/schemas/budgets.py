from pydantic import Field, BaseModel
from decimal import Decimal


class GetBudgetsRequest(BaseModel):
	user_id: int
	period: str = Field(min_length=7, max_length=7, pattern=r"^\d{4}-\d{2}$")


class CreateBudgetRequest(BaseModel):
	user_id: int
	category_id: int
	period: str = Field(min_length=7, max_length=7, pattern=r"^\d{4}-\d{2}$")
	limit: Decimal = Field(gt = 0)


class BudgetResponse(BaseModel):
	id: int
	category: str
	period: str
	limit: Decimal
