from flask import Blueprint, request

from app.services.budget_service import get_budgets, create_budget

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')

@budgets_bp.get('/get_budgets')
def get():
	data = request.get_json() or {}
	user_id = data.get("user_id")
	period = data.get("period")
	if not user_id or not period:
		return {"message": "user_id and period are required"}, 400
	result = get_budgets(user_id, period)
	return result, 200

@budgets_bp.post('/create_budget')
def create():
	data = request.get_json() or {}

	user_id = data.get("user_id")
	category_id = data.get("category_id")
	period = data.get("period")
	limit = data.get("limit")

	if not user_id or not category_id or not period or not limit:
		return {"message": "user_id, category_id, period and limit are required"}, 400
	result = create_budget(user_id, category_id, period, limit)
	return result, 201