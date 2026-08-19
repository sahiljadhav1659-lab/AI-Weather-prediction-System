import sqlite3
from datetime import datetime

DATABASE = "database/weather.db"

def migrate_dates():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, prediction_date FROM prediction_history")
    rows = cursor.fetchall()

    fixed = 0
    already_ok = 0
    failed = 0

    for row_id, date_str in rows:
        # आधीच YYYY-MM-DD फॉरमॅटमध्ये आहे का ते तपासा
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            already_ok += 1
            continue
        except (ValueError, TypeError):
            pass

        # DD-MM-YYYY फॉरमॅटमध्ये आहे का ते तपासून बदला
        try:
            dt = datetime.strptime(date_str, "%d-%m-%Y")
            new_date = dt.strftime("%Y-%m-%d")
            cursor.execute(
                "UPDATE prediction_history SET prediction_date = ? WHERE id = ?",
                (new_date, row_id)
            )
            fixed += 1
        except (ValueError, TypeError):
            print(f"Could not parse row id={row_id}, date={date_str}")
            failed += 1

    conn.commit()
    conn.close()

    print(f"आधीच बरोबर होते: {already_ok}")
    print(f"दुरुस्त केले: {fixed}")
    print(f"दुरुस्त होऊ शकले नाहीत: {failed}")

if __name__ == "__main__":
    migrate_dates()