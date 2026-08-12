import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("dataset/clean_weather.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# -------------------------------
# Graph 1: Maximum Temperature Trend
# -------------------------------
plt.figure(figsize=(12,5))
plt.plot(df["date"], df["temperature_2m_max"])
plt.title("Maximum Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/temperature_trend.png")
plt.close()

# -------------------------------
# Graph 2: Minimum Temperature Trend
# -------------------------------
plt.figure(figsize=(12,5))
plt.plot(df["date"], df["temperature_2m_min"])
plt.title("Minimum Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/min_temperature_trend.png")
plt.close()

# -------------------------------
# Graph 3: Rainfall Trend
# -------------------------------
plt.figure(figsize=(12,5))
plt.plot(df["date"], df["rain_sum"])
plt.title("Rainfall Trend")
plt.xlabel("Date")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/rainfall_trend.png")
plt.close()

# -------------------------------
# Graph 4: Wind Speed Trend
# -------------------------------
plt.figure(figsize=(12,5))
plt.plot(df["date"], df["wind_speed_10m_max"])
plt.title("Wind Speed Trend")
plt.xlabel("Date")
plt.ylabel("Wind Speed")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/wind_speed_trend.png")
plt.close()

# -------------------------------
# Graph 5: Temperature Histogram
# -------------------------------
plt.figure(figsize=(8,5))
plt.hist(df["temperature_2m_max"], bins=30)
plt.title("Maximum Temperature Distribution")
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("graphs/temperature_histogram.png")
plt.close()

print("✅ All graphs generated successfully!")
print("Graphs are saved inside the 'graphs' folder.")