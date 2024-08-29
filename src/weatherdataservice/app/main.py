from fastapi import FastAPI
from .routers import weather
from .database import Base, engine
from .tasks import fetch_and_store_weather

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(weather.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather Data Service!"}

@app.on_event("startup")
def startup_event():
    # Schedule periodic fetching every hour
    fetch_and_store_weather.apply_async(("New York",), countdown=3600)
