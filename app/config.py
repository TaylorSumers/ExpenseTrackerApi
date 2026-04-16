from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	APP_NAME: str = 'Expense Tracker API'
	DEBUG: bool = True
	JWT_SECRET_KEY: str = "enter jwt secret here"
	JWT_ALGORITHM: str = 'HS256'
	JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
	DB_NAME: str = "ExpenseTracker.db"


	@property
	def database_url(self) -> str:
		return f"sqlite+aiosqlite:///{self.DB_NAME}"

	@property
	def alembic_database_url(self) -> str:
		return f"sqlite:///{self.DB_NAME}"

	model_config = SettingsConfigDict(env_file=".env")

settings = Settings()