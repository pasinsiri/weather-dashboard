from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.weather import get_weather
from utils.location import get_location_from_ip
import os

