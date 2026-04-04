from flask import Flask, jsonify
from app.config import settings
from app.routes.auth import auth_bp
from app.routes.budgets import budgets_bp
from app.routes.categories import categories_bp
from app.routes.transactions import transactions_bp


def create_app() -> Flask:
	app = Flask(__name__)
	app.config['SECRET_KEY'] = settings.SECRET_KEY
	app.config['DEBUG'] = settings.DEBUG
	# app.config["JSON_AS_ASCII"] = False

	register_blueprints(app)
	register_error_handlers(app)

	return app


def register_blueprints(app: Flask) -> None:
	app.register_blueprint(auth_bp)
	app.register_blueprint(categories_bp)
	app.register_blueprint(transactions_bp)
	app.register_blueprint(budgets_bp)


def register_error_handlers(app: Flask) -> None:
	@app.errorhandler(404)
	def not_found(_error):
		return jsonify({'message': 'Not found'}), 404

	@app.errorhandler(500)
	def internal_error(_error):
		return jsonify({'message': 'Internal Server Error'}), 500
