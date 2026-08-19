import sqlite3
import random
from datetime import date, timedelta

DATABASE = "database/weather.db"

# =====================================================
# DEMO WEATHER DATA
# =====================================================

cities = [
    "Pune",
    "Mumbai",
    "Nashik",
    "Satara"
]

predictions = [
    "Rain Expected",
    "No Rain",
    "Light Rain",
    "Heavy Rain"
]

# Today
end_date = date.today()

# Approximately previous 2 months
start_date = end_date - timedelta(days=59)

records = []

current_date = start_date

while current_date <= end_date:

    # Random number of observations per day
    # 1-2 records per day
    daily_records = random.choice([1, 1, 2])

    for _ in range(daily_records):

        city = random.choice(cities)

        # Temperature
        temperature = round(random.uniform(20, 34), 1)

        # Humidity
        humidity = round(random.uniform(45, 90), 1)

        # Wind speed
        wind_speed = round(random.uniform(5, 30), 1)

        # Rainfall
        rainfall = round(random.uniform(0, 25), 1)

        # Prediction based roughly on rainfall
        if rainfall >= 15:
            prediction = "Heavy Rain"

        elif rainfall >= 5:
            prediction = "Rain Expected"

        elif rainfall > 0:
            prediction = "Light Rain"

        else:
            prediction = "No Rain"

        # Random time
        hour = random.randint(7, 20)
        minute = random.randint(0, 59)

        prediction_time = f"{hour:02d}:{minute:02d}:00"

        records.append((
            current_date.strftime("%Y-%m-%d"),
            prediction_time,
            city,
            temperature,
            humidity,
            wind_speed,
            rainfall,
            prediction
        ))

    current_date += timedelta(days=1)


# =====================================================
# INSERT INTO DATABASE
# =====================================================

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

cursor.executemany("""
    INSERT INTO prediction_history(
        prediction_date,
        prediction_time,
        city,
        temperature,
        humidity,
        wind_speed,
        rainfall,
        prediction
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", records)

conn.commit()

conn.close()


print()
print("=" * 55)
print("DEMO WEATHER DATA INSERTED SUCCESSFULLY")
print("=" * 55)
print(f"Start Date : {start_date}")
print(f"End Date   : {end_date}")
print(f"Records    : {len(records)}")
print("=" * 55)