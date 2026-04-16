from http import HTTPStatus
from flask import Blueprint

from app.auth.decorators import auth_required, get_current_user
from app.common.money import from_minor_unites
from app.responses import success_response
from app.schemas.transactions import GetTransactionRequest, TransactionResponse, CreateTransactionRequest, \
	DeleteTransactionRequest
from app.services.transaction_service import get_transaction, create_transaction, delete_transaction
from app.validation import validate_body, validate_query

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@transactions_bp.get('/get_transaction')
@auth_required
async def get():
	current_user = get_current_user()
	payload = validate_query(GetTransactionRequest)
	transaction = await get_transaction(payload.transaction_id, current_user.id)
	response = TransactionResponse(
		id=transaction.id,
		category=transaction.category.name if transaction.category else None,
		amount=from_minor_unites(transaction.amount),
		type=transaction.type,
		description=transaction.description,
		executed_at=transaction.executed_at,
		created_at=transaction.created_at
	)
	return success_response(response.model_dump())


@transactions_bp.post('/create_transaction')
@auth_required
async def create():
	current_user = get_current_user()
	payload = validate_body(CreateTransactionRequest)
	await create_transaction(
		current_user.id,
		payload.category_id,
		payload.amount,
		payload.type,
		payload.description,
		payload.executed_at
	)
	return success_response(status_code=HTTPStatus.CREATED)


@transactions_bp.delete('/delete_transaction')
@auth_required
async def delete():
	current_user = get_current_user()
	payload = validate_body(DeleteTransactionRequest)
	await delete_transaction(payload.transaction_id, current_user.id)
	return success_response(status_code=HTTPStatus.NO_CONTENT)