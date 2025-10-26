import os
from dotenv import load_dotenv
import requests

load_dotenv()

def get_weather(city):
    api_key = os.environ.get("OPEN_WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()

        return {
            "city": data["name"],
            "temperature": round(data["main"]["temp"], 1),
            "condition": data["weather"][0]["description"]
        }
    except:
        return {"error": f"Couldn't get weather for {city}"}
