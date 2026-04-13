from http import HTTPStatus

from flask import Blueprint

from app.common.money import from_minor_unites
from app.responses import success_response
from app.schemas.budgets import GetBudgetsRequest, BudgetResponse, CreateBudgetRequest
from app.services.budget_service import get_budgets, create_budget
from app.validation import validate_body, validate_query

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')


@budgets_bp.get('/get_budgets')
async def get():
	payload = validate_query(GetBudgetsRequest)
	budgets = await get_budgets(payload.user_id, payload.period)
	response = [BudgetResponse(
		id=budget.id,
		category=budget.category.name,
		period=budget.period,
		limit=from_minor_unites(budget.limit)
	).model_dump() for budget in budgets]
	return success_response(response)


@budgets_bp.post('/create_budget')
async def create():
	payload = validate_body(CreateBudgetRequest)
	await create_budget(payload.user_id, payload.category_id, payload.period, payload.limit)
	return success_response(status_code=HTTPStatus.CREATED)
