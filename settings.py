from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Student Course Management API"
    debug: bool = False

    model_config = SettingsConfigDict(env_file="app_config.env", extra="ignore")

settings = Settings()