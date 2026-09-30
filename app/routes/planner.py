from fastapi import APIRouter

router = APIRouter(prefix="/plan", tags=["Travel Plan"])


@router.post("/")
async def create_travel_plan():
    """Aggregate Weather, Currency, and Places data into a single travel plan."""
    return {
        "message":"Travel plan created successfully"
    }