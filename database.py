import sqlite3
import os

# ---------------- DATABASE PATH ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

# Create database folder if it doesn't exist
os.makedirs(DATABASE_DIR, exist_ok=True)

DATABASE = os.path.join(DATABASE_DIR, "weather.db")


# ---------------- CREATE TABLE ----------------

def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Prediction History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        prediction_date TEXT,
        prediction_time TEXT,
        city TEXT,
        temperature REAL,
        humidity REAL,
        wind_speed REAL,
        rainfall REAL,
        prediction TEXT

    )
    """)

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL

    )
    """)

    # Admins Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL

    )
    """)

    conn.commit()
    conn.close()


# ---------------- INSERT PREDICTION ----------------

def insert_prediction(
    prediction_date,
    prediction_time,
    city,
    temperature,
    humidity,
    wind_speed,
    rainfall,
    prediction
):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

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
        city,
        temperature,
        humidity,
        wind_speed,
        rainfall,
        prediction
    ))

    conn.commit()
    conn.close()


# ---------------- GET ALL PREDICTIONS ----------------

def get_all_predictions():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM prediction_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


# ---------------- REGISTER USER ----------------

def register_user(full_name, email, password):

    conn = sqlite3.connect(DATABASE, timeout=10)

    try:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users(full_name, email, password)
            VALUES(?,?,?)
        """, (full_name, email, password))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ---------------- LOGIN USER ----------------

def login_user(email, password):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user


# ---------------- GET ALL USERS ----------------

def get_all_users():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, full_name, email, password
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return users


# ---------------- ADD ADMIN ----------------

def add_admin(username, password):

    conn = sqlite3.connect(DATABASE)

    try:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO admins(username, password)
            VALUES(?, ?)
        """, (username, password))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()