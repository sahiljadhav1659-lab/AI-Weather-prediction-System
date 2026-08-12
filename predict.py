import joblib
import pandas as pd

# Load the trained model
model = joblib.load("models/weather_model.pkl")

print("===== Weather Prediction System =====")

# Get user input
temperature_2m_max = float(input("Enter Maximum Temperature (°C): "))
temperature_2m_min = float(input("Enter Minimum Temperature (°C): "))
apparent_temperature_max = float(input("Enter Apparent Maximum Temperature (°C): "))
apparent_temperature_min = float(input("Enter Apparent Minimum Temperature (°C): "))
precipitation_sum = float(input("Enter Precipitation (mm): "))
wind_speed_10m_max = float(input("Enter Maximum Wind Speed (km/h): "))
wind_gusts_10m_max = float(input("Enter Maximum Wind Gust (km/h): "))
weather_code = int(input("Enter Weather Code: "))

# Create DataFrame
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

# Predict
prediction = model.predict(input_data)

print("\n===== Prediction Result =====")

if prediction[0] == 1:
    print("🌧️ Rain Expected")
else:
    print("☀️ No Rain Expected")