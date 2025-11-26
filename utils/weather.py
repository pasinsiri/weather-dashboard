import httpx
from typing import Dict, Any

async def get_weather(city: str, api_key: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        # First get coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        try:
            geo_response = await client.get(geo_url)
            geo_response.raise_for_status()
            geo_resp = geo_response.json()
        except Exception as e:
            return {"error": f"Failed to fetch location: {str(e)}"}

        if not geo_resp:
            return {"error": "City not found"}

        lat, lon = geo_resp[0]["lat"], geo_resp[0]["lon"]

        # Now get weather
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )

        try:
            current_response = await client.get(weather_url)
            current_response.raise_for_status()
            current = current_response.json()

            forecast_response = await client.get(forecast_url)
            forecast_response.raise_for_status()
            forecast = forecast_response.json()
        except Exception as e:
            return {"error": f"Failed to fetch weather data: {str(e)}"}

        return {
            "city": current["name"],
            "country": current["sys"]["country"],
            "temp": round(current["main"]["temp"]),
            "feels_like": round(current["main"]["feels_like"]),
            "description": current["weather"][0]["description"].title(),
            "icon": current["weather"][0]["icon"],
            "humidity": current["main"]["humidity"],
            "wind_speed": current["wind"]["speed"],
            "forecast": [
                {
                    "date": item["dt_txt"].split(" ")[0],
                    "temp": round(item["main"]["temp"]),
                    "icon": item["weather"][0]["icon"],
                    "desc": item["weather"][0]["description"].title()
                }
                for item in forecast["list"][::8]  # Every 24h (8 × 3h)
            ][:5]
        }