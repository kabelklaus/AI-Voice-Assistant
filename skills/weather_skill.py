# weather_skill.py

import requests
from dotenv import load_dotenv
import os

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

def get_current_weather(location):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "API-Schlüssel nicht gefunden."
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={location}&appid={api_key}&lang=de&units=metric"
    
    print(f"API-Anfrage: {complete_url}")  # Debug-Ausgabe der API-Anfrage
    
    response = requests.get(complete_url)
    data = response.json()
    
    print(f"API-Antwort: {data}")  # Debug-Ausgabe der API-Antwort

    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        feels_like = main["feels_like"]
        temp_min = main["temp_min"]
        temp_max = main["temp_max"]
        humidity = main["humidity"]
        description = weather["description"]
        clouds = data["clouds"]["all"]

        return (f"In {location} sind es {temperature} Grad (gefühlt {feels_like} Grad) und {description}. "
                f"Der Bewölkungsgrad liegt bei {clouds} Prozent. "
                f"Die minimale Temperatur beträgt {temp_min} Grad und es wird maximal {temp_max} Grad. "
                f"Die Luftfeuchtigkeit liegt bei {humidity} Prozent.")
    else:
        return "Stadt nicht gefunden."
