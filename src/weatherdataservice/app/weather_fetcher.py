import requests
from .config import settings
from .database import SessionLocal, redis_client, mongo_db
from .models import WeatherData
from datetime import datetime

def fetch_weather_data(city: str):
    url = f"{settings.WEATHER_API_URL}?key={settings.WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_data = {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "condition": data["current"]["condition"]["text"],
            "timestamp": datetime.utcnow()
        }
        store_in_postgres(weather_data)
        store_in_mongo(weather_data)
        cache_in_redis(weather_data)
    else:
        print(f"Error fetching weather data: {data}")

def store_in_postgres(weather_data):
    db = SessionLocal()
    db_weather = WeatherData(**weather_data)
    db.add(db_weather)
    db.commit()
    db.close()

def store_in_mongo(weather_data):
    mongo_db.weather_data.insert_one(weather_data)

def cache_in_redis(weather_data):
    redis_key = f"weather:{weather_data['city']}"
    redis_client.set(redis_key, str(weather_data), ex=3600)  # Cache for 1 hour
