from flask import Blueprint, request

from app.services.transaction_service import get_transaction, create_transaction, delete_transaction

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# @transactions_bp.get()
# async def get():
# 	data = request.get_json() or {}
# 	transaction_id = data["transaction_id"]
# 	if not transaction_id:
# 		return {"message": "transaction_id is required"}, 400
# 	result = await get_transaction(transaction_id)
# 	return result, 200
#
# @transactions_bp.post()
# async def create():
# 	data = request.get_json() or {}
# 	user_id = data['user_id']
# 	category_id = data['category_id']
# 	amount = data['amount']
# 	type = data['type']
# 	description = data['description']
# 	executed_at = data['executed_at']
# 	if not user_id or not amount or not type or not executed_at:
# 		return {"message": "user_id, amount, type and executed_at are required"}, 400
# 	await create_transaction(user_id, category_id, amount, type, description, executed_at)
# 	return 201
#
# @transactions_bp.delete()
# async def delete():
# 	data = request.get_json() or {}
# 	transaction_id = data['transaction_id']
# 	if not transaction_id:
# 		return {"message": "transaction_id is required"}, 400
# 	await delete_transaction(transaction_id)
# 	return 200