from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WEATHER_API_URL: str
    WEATHER_API_KEY: str
    POSTGRES_URL: str
    MONGO_URL: str
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file = ".env"

settings = Settings()
