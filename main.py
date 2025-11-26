from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.weather import get_weather
from utils.location import get_location_from_ip
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    location = get_location_from_ip()
    weather = await get_weather(location, os.getenv("OPENWEATHER_API_KEY"))
    return templates.TemplateResponse("index.html", {
        "request": request,
        "weather": weather,
        "location": location
    })

