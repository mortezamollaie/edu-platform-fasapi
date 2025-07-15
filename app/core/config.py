from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EduPlatform"
    DATABASE_URL: str = "sqlite:///./db.sqlite3"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()        