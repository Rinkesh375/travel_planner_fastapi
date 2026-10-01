import httpx
from datetime import date
from app.model import WeatherResponseModel
from config import settings
from app.services.cache import get_cache, set_cache


async def fetch_weather(
    destination: str, start_date: date, end_date: date
) -> list[WeatherResponseModel]:
    
    cache_key = f"{destination}_{start_date}_{end_date}"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return cached_data
        

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.weatherapi.com/v1/forecast.json",
            params={
                "key": settings.weather_api_key,
                "q": destination,
                "dt": start_date,
                "end_date": end_date,
            },
        )

        response.raise_for_status()

        data = response.json()
        forecasts = []
        
        print(f"weather api response data:{data}")

        for day in data["forecast"]["forecastday"]:
            forecast = WeatherResponseModel(
                date=day["date"],
                condition=day["day"]["condition"]["text"],
                temperature_high=day["day"]["maxtemp_c"],
                temperature_low=day["day"]["mintemp_c"],
                humidity=day["day"]["avghumidity"],
                rain_chance=day["day"]["daily_chance_of_rain"],
            )

            forecasts.append(forecast)
            
        # cache data for 1 hour
        set_cache(cache_key,forecasts,ttl=3600)    

        return forecasts
