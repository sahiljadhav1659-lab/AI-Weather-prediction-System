import joblib
import pandas as pd
from datetime import date

# Load the trained model
model = joblib.load("models/weather_model.pkl")


# ==========================================
# SEASON DETECTION
# ==========================================

def get_season(month):
    if month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    elif month == 10:
        return "Post-Monsoon"
    else:
        return "Winter"


print("===== Weather Prediction System =====")

# Today's date
today = date.today()

print(f"\n📅 Date: {today.strftime('%d-%m-%Y')}")

season = get_season(today.month)

print(f"🌤️ Current Season: {season}")


# ==========================================
# GET USER INPUT
# ==========================================

temperature_2m_max = float(input("Enter Maximum Temperature (°C): "))
temperature_2m_min = float(input("Enter Minimum Temperature (°C): "))
apparent_temperature_max = float(input("Enter Apparent Maximum Temperature (°C): "))
apparent_temperature_min = float(input("Enter Apparent Minimum Temperature (°C): "))
precipitation_sum = float(input("Enter Precipitation (mm): "))
wind_speed_10m_max = float(input("Enter Maximum Wind Speed (km/h): "))
wind_gusts_10m_max = float(input("Enter Maximum Wind Gust (km/h): "))
weather_code = int(input("Enter Weather Code: "))


# ==========================================
# CREATE DATAFRAME
# ==========================================

input_data = pd.DataFrame({
    "temperature_2m_max": [temperature_2m_max],
    "temperature_2m_min": [temperature_2m_min],
    "apparent_temperature_max": [apparent_temperature_max],
    "apparent_temperature_min": [apparent_temperature_min],
    "precipitation_sum": [precipitation_sum],
    "wind_speed_10m_max": [wind_speed_10m_max],
    "wind_gusts_10m_max": [wind_gusts_10m_max],
    "weather_code": [weather_code]
})


# ==========================================
# RAIN PREDICTION
# ==========================================

prediction = model.predict(input_data)


# ==========================================
# FINAL RESULT
# ==========================================

print("\n===== Prediction Result =====")

if prediction[0] == 1:
    print("🌧️ Rain Expected")
else:
    print("☀️ No Rain Expected")

print(f"🌤️ Season: {season}")

if season == "Winter":
    print("❄️ Winter conditions are expected.")
elif season == "Summer":
    print("☀️ Summer conditions are expected.")
elif season == "Monsoon":
    print("🌧️ Monsoon season is active.")
else:
    print("🍂 Post-Monsoon season is active.")