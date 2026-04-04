from flask import Flask
from app.routes.auth import auth_bp
from app.routes.budgets import budgets_bp
from app.routes.categories import categories_bp
from app.routes.transactions import transactions_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(budgets_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(transactions_bp)

if __name__ == '__main__':
	app.run(debug=True)