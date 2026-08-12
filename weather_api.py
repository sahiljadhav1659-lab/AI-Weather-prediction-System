import requests
from datetime import datetime

cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
}

def get_weather(city="Delhi", latitude=None, longitude=None):
    if latitude is None or longitude is None:
        key = city.strip().title()
        if key not in cities:
            raise ValueError(f"Unknown city '{city}'. Choose from: {list(cities)}")
        latitude, longitude = cities[key]

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,rain,weather_code"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Weather API error: {e}")
        return None

    data = response.json()
    weather_code = data["current"]["weather_code"]

    if weather_code == 0:
        icon, condition = "☀️", "Clear Sky"
    elif weather_code in (1, 2, 3):
        icon, condition = "⛅", "Partly Cloudy"
    elif weather_code in (45, 48):
        icon, condition = "🌫️", "Fog"
    elif weather_code in (51, 53, 55, 61, 63, 65):
        icon, condition = "🌧️", "Rain"
    elif weather_code in (71, 73, 75):
        icon, condition = "❄️", "Snow"
    elif weather_code in (95, 96, 99):
        icon, condition = "⛈️", "Thunderstorm"
    else:
        icon, condition = "🌤️", "Live Weather"

    current = data["current"]
    return {
        "city": city,
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "rain": current["rain"],
        "rainfall": current["rain"],
        "condition": condition,
        "icon": icon,
        "time": datetime.now().strftime("%I:%M %p"),
    }