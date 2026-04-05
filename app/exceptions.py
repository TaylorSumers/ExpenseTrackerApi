from http import HTTPStatus


class ApiError(Exception):
	status_code = HTTPStatus.INTERNAL_SERVER_ERROR
	code = 'internal_error'
	message = 'Internal server error'

	def __init__(self, message: str | None = None, *, code: str | None = None):
		super().__init__(message or self.message)
		self.message = message or self.message
		self.code = code or self.code


class BadRequestError(ApiError):
	status_code = HTTPStatus.BAD_REQUEST
	code = 'bad_request'
	message = 'Bad request'


class UnauthorizedError(ApiError):
	status_code = HTTPStatus.UNAUTHORIZED
	code = 'unauthorized'
	message = 'Unauthorized'


class NotFoundError(ApiError):
	status_code = HTTPStatus.NOT_FOUND
	code = 'not_found'
	message = 'Resource not found'


class ConflictError(ApiError):
	status_code = HTTPStatus.CONFLICT
	code = 'conflict'
	message = 'Conflict'
