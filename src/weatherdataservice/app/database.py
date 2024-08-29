from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import redis

from .config import settings

# PostgreSQL Setup
engine = create_engine(settings.POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Setup
mongo_client = MongoClient(settings.MONGO_URL)
mongo_db = mongo_client.weather_db

# Redis Setup
redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)
