from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ..database import SessionLocal, redis_client
from ..models import WeatherDataResponse, WeatherData
import json

router = APIRouter()

@router.get("/weather")
def get_weather():
    return {"data": "Sample weather data"}

@router.get("/weather/{city}", response_model=WeatherDataResponse)
def get_weather_data(
    city: str, 
    local_kw: str = Query(None),  # Optional query parameter
    db: Session = Depends(SessionLocal)  # Database session dependency
):
    print(f"Received city: {city}, local_kw: {local_kw}")

    # Caching logic
    redis_key = f"weather:{city}"
    cached_data = redis_client.get(redis_key)

    if cached_data:
        return json.loads(cached_data)

    # Fetch weather data from the database
    db_weather = db.query(WeatherData).filter(WeatherData.city == city).order_by(WeatherData.timestamp.desc()).first()

    if not db_weather:
        raise HTTPException(status_code=404, detail="Weather data not found")

    response = WeatherDataResponse.from_orm(db_weather)

    # Cache the response in Redis
    redis_client.set(redis_key, response.json(), ex=3600)

    return response
