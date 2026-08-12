import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

# Load model
model = joblib.load("models/weather_model.pkl")

# Load processed dataset
df = pd.read_csv("dataset/weather_cleaned.csv")

# Features
X = df[
    [
        "temperature_2m_max",
        "temperature_2m_min",
        "apparent_temperature_max",
        "apparent_temperature_min",
        "precipitation_sum",
        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "weather_code"
    ]
]

# Target
y = df["Rain"]

# Prediction
pred = model.predict(X)

accuracy = accuracy_score(y, pred)

print("Accuracy :", round(accuracy * 100, 2), "%")