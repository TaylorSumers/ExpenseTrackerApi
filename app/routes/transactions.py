from http import HTTPStatus

from flask import Blueprint, request

from app.exceptions import BadRequestError
from app.responses import success_response
from app.services.transaction_service import get_transaction, create_transaction, delete_transaction

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@transactions_bp.get('/get_transaction')
async def get():
	data = request.get_json() or {}

	transaction_id = data["transaction_id"]

	if not transaction_id:
		BadRequestError("transaction_id is required")

	transaction = await get_transaction(transaction_id)
	return success_response({
		'category': transaction.category.name,
		'amount': transaction.amount,
		'type': transaction.type,
		'description': transaction.description,
		'executed_at': transaction.executed_at
	})


@transactions_bp.post('/create_transaction')
async def create():
	data = request.get_json() or {}

	user_id = data['user_id']
	category_id = data['category_id']
	amount = data['amount']
	type = data['type']
	description = data['description']
	executed_at = data['executed_at']

	if not user_id or not amount or not type or not executed_at:
		BadRequestError("user_id, amount, type and executed_at are required")

	await create_transaction(user_id, category_id, amount, type, description, executed_at)
	return success_response(status_code=HTTPStatus.CREATED)


@transactions_bp.delete('/delete_transaction')
async def delete():
	data = request.get_json() or {}

	transaction_id = data['transaction_id']

	if not transaction_id:
		BadRequestError("transaction_id is required")

	await delete_transaction(transaction_id)
	return success_response(status_code=HTTPStatus.NO_CONTENT)