from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	APP_NAME: str = 'Expense Tracker API'
	DEBUG: bool = True
	SECRET_KEY: str
	DB_NAME: str = "ExpenseTracker.db"

	@property
	def database_url(self):
		return f"sqlite+aiosqlite:///{self.DB_NAME}"

	model_config = SettingsConfigDict(env_file=".env")

settings = Settings()