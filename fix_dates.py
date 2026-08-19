import sqlite3
from datetime import datetime

DATABASE = "database/weather.db"

def insert_test_record():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    prediction_date = datetime.now().strftime("%d-%m-%Y")
    prediction_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute("""
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
        VALUES(?,?,?,?,?,?,?,?)
    """, (
        prediction_date,
        prediction_time,
        "Kolhapur",
        29.5,
        65.0,
        12.3,
        0.0,
        "No Rain"
    ))

    conn.commit()
    conn.close()
    print(f"Inserted record with date: {prediction_date}")

if __name__ == "__main__":
    insert_test_record()