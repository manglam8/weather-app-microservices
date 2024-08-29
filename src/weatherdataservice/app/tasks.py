from celery import Celery
from .config import settings
from .weather_fetcher import fetch_weather_data

celery_app = Celery(
    "weather_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery_app.task
def fetch_and_store_weather(city: str):
    fetch_weather_data(city)
