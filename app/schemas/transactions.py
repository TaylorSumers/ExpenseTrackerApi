from decimal import Decimal
from datetime import datetime
from enum import Enum

from pydantic import Field

from app.schemas.base import ResponseSchema, RequestSchema


class TransactionType(str, Enum):
	income = 'income'
	expense = 'expense'


class GetTransactionRequest(RequestSchema):
	transaction_id: int


class DeleteTransactionRequest(RequestSchema):
	transaction_id: int


class CreateTransactionRequest(RequestSchema):
	user_id: int
	category_id: int
	amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
	type: TransactionType
	description: str | None = Field(default=None, max_length=500)
	executed_at: datetime


class TransactionResponse(ResponseSchema):
	id: int
	category: str | None
	amount: Decimal
	type: TransactionType
	description: str | None
	executed_at: datetime
	created_at: datetime
