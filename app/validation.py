from typing import Type

from flask import request
from pydantic import ValidationError

from app.exceptions import BadRequestError
from app.schemas.base import RequestSchema


def validate_body(schema_cls: Type[RequestSchema]) -> RequestSchema:
	raw_data = request.get_json(silent=True)
	if raw_data is None:
		raise BadRequestError("Request body must be valid JSON")

	try:
		return schema_cls.model_validate(raw_data)
	except ValidationError as exc:
		raise BadRequestError(f"Validation error: {exc}") from exc


def validate_query(schema_cls: Type[RequestSchema]) -> RequestSchema:
	raw_data = request.args.to_dict(flat=True)

	try:
		return schema_cls.model_validate(raw_data)
	except ValidationError as exc:
		raise BadRequestError(f"Validation error: {exc}") from exc