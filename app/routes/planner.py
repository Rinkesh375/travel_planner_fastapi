from fastapi import APIRouter, HTTPException
from app.model import TravelRequestModel
from app.services.weather import fetch_weather

router = APIRouter(prefix="/plan", tags=["Travel Plan"])


@router.post("/")
async def create_travel_plan(travel_request: TravelRequestModel):
    """Aggregate Weather, Currency, and Places data into a single travel plan."""

    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date",
        )

    trip_days = (travel_request.end_date - travel_request.start_date).days

    if trip_days < 1:
        raise HTTPException(
            status_code=400,
            detail="Travel plan must be at least 1 day long",
        )

    if trip_days > 14:
        raise HTTPException(
            status_code=400,
            detail="Travel plan cannot be longer than 14 days",
        )
    
    weather_data = await fetch_weather(
        destination=travel_request.destination,
        start_date=travel_request.start_date,
        end_date=travel_request.end_date
    )
    return {
        "message": "Travel plan created successfully",
        "weather_data":weather_data    
    }
