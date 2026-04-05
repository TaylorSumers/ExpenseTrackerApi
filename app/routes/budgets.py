from http import HTTPStatus

from flask import Blueprint, request

from app.exceptions import BadRequestError
from app.responses import success_response
from app.services.budget_service import get_budgets, create_budget

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')

@budgets_bp.get('/get_budgets')
async def get():
	data = request.get_json() or {}

	user_id = data.get("user_id")
	period = data.get("period")

	if not user_id or not period:
		raise BadRequestError("user_id and period are required")

	budgets = await get_budgets(user_id, period)
	return success_response({{
		'category': budget.category.name,
		'period': budget.period,
		'limit': budget.limit
	} for budget in budgets})

@budgets_bp.post('/create_budget')
async def create():
	data = request.get_json() or {}

	user_id = data.get("user_id")
	category_id = data.get("category_id")
	period = data.get("period")
	limit = data.get("limit")

	if not user_id or not category_id or not period or not limit:
		raise BadRequestError("user_id, category_id, period and limit are required")

	await create_budget(user_id, category_id, period, limit)
	return success_response(status_code=HTTPStatus.CREATED)