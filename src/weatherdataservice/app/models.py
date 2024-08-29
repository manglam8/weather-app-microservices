from sqlalchemy import Column, Integer, String, Float, DateTime
from pydantic import BaseModel
from .database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    region = Column(String)
    country = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    condition = Column(String)
    timestamp = Column(DateTime)

class WeatherDataResponse(BaseModel):
    city: str
    region: str
    country: str
    temperature: float
    humidity: float
    condition: str
    timestamp: str

    class Config:
        orm_mode = True
