import httpx

def get_location_from_ip():
    try:
        response = httpx.get("https://ipinfo.io/json")
        data = response.json()
        city = data.get("city", "London")
        country = data.get("country", "GB")
        return f"{city}, {country}"
    except:
        return "London, GB"