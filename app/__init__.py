from flask import Flask
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
import logging

from app.config import settings
from app.database import init_db
from app.exceptions import ApiError, ConflictError
from app.responses import error_response
from app.routes.auth import auth_bp
from app.routes.budgets import budgets_bp
from app.routes.categories import categories_bp
from app.routes.transactions import transactions_bp


def create_app(test_config: dict | None = None) -> Flask:
	app = Flask(__name__)
	app.config.from_mapping(
		TESTING=False,
		DEBUG=settings.DEBUG,
		SECRET_KEY=settings.SECRET_KEY,
		DATABASE_URL=settings.database_url,
	)

	if test_config:
		app.config.update(test_config)

	init_db(app.config['DATABASE_URL'])
	register_blueprints(app)
	register_error_handlers(app)

	@app.get('/health')
	async def healthcheck():
		return {"status": "ok"}, 200

	return app


def register_blueprints(app: Flask) -> None:
	app.register_blueprint(auth_bp)
	app.register_blueprint(categories_bp)
	app.register_blueprint(transactions_bp)
	app.register_blueprint(budgets_bp)


def register_error_handlers(app: Flask) -> None:
	logger = logging.getLogger(__name__)

	def build_api_error_response(error: ApiError):
		return error_response(
			message=error.message,
			code=error.code,
			status_code=error.status_code,
		)

	@app.errorhandler(ApiError)
	def handle_api_error(error: ApiError):
		return build_api_error_response(error)

	@app.errorhandler(IntegrityError)
	def handle_integrity_error(_error: IntegrityError):
		conflict = ConflictError('Resource already exists')
		return error_response(message=conflict.message, code=conflict.code, status_code=conflict.status_code)

	@app.errorhandler(HTTPException)
	def handle_http_exception(error: HTTPException):
		return error_response(message=error.description, code=error.name.lower().replace(' ', '_'), status_code=error.code)

	@app.errorhandler(Exception)
	def handle_unexpected_error(error: Exception):
		logger.error('Unexpected error', exc_info=error)
		return build_api_error_response(ApiError())

