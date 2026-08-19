import sqlite3

conn = sqlite3.connect("database/weather.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM prediction_history")
print("Total records:", cursor.fetchone()[0])
conn.close()