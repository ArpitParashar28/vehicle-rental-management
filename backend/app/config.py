from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Portfolio API"
    database_url: str = "sqlite:///./app.db"
    cors_origins: str = "http://localhost:5173"
    secret_key: str = "change-me-in-production"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
