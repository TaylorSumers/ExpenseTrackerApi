from http import HTTPStatus

from flask import Blueprint

from app.auth.decorators import auth_required, get_current_user
from app.common.money import from_minor_unites
from app.responses import success_response
from app.schemas.budgets import GetBudgetsRequest, BudgetResponse, CreateBudgetRequest
from app.services.budget_service import get_budgets, create_budget
from app.validation import validate_body, validate_query

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')


@budgets_bp.get('/get_budgets')
@auth_required
async def get():
	current_user = get_current_user()
	payload = validate_query(GetBudgetsRequest)
	budgets = await get_budgets(current_user.id, payload.period)
	response = [BudgetResponse(
		id=budget.id,
		category=budget.category.name,
		period=budget.period,
		limit=from_minor_unites(budget.limit)
	).model_dump() for budget in budgets]
	return success_response(response)


@budgets_bp.post('/create_budget')
@auth_required
async def create():
	current_user = get_current_user()
	payload = validate_body(CreateBudgetRequest)
	await create_budget(current_user.id, payload.category_id, payload.period, payload.limit)
	return success_response(status_code=HTTPStatus.CREATED)
