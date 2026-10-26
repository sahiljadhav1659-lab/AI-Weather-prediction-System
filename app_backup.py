from flask import Flask, render_template, request, send_file, redirect, session, jsonify
import os
import requests
import os
import csv
import joblib
import pandas as pd
from datetime import datetime
from collections import defaultdict
from database import get_all_users

from pdf_generator import generate_pdf
from history_pdf import generate_history_pdf
from weather_api import get_weather

from database import (
    create_table,
    insert_prediction,
    get_all_predictions,
    register_user,
    login_user,
    get_all_users
)
app = Flask(__name__)
print("ROOT:", app.root_path)
print("TEMPLATES:", app.template_folder)
app.secret_key = "weather_prediction_secret_key_2026"

# ==================================================
# CREATE DATABASE
# ==================================================
create_table()

# ==================================================
# LOAD MODEL
# ==================================================
model = joblib.load("models/weather_model.pkl")

# ==================================================
# HOME
# ==================================================
@app.route("/")
def home():

    city = "Delhi"

    weather = get_weather(city)

    return render_template(
        "index.html",
        weather=weather,
        city=city
    )

# ==================================================
# ABOUT
# ==================================================
@app.route("/about")
def about():
    return render_template("about.html")


# ==================================================
# DASHBOARD
# ==================================================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    accuracy = "98.43%"
    dataset_records = 91320
    total_features = 8
    algorithm = "Random Forest"

    city = request.args.get("city", "Delhi")
    weather = get_weather(city)

    # Display-only date, not saved to DB - format kept as DD-MM-YYYY for readability
    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M %p")

    return render_template(
        "dashboard.html",
        accuracy=accuracy,
        dataset_records=dataset_records,
        total_features=total_features,
        algorithm=algorithm,
        current_date=current_date,
        current_time=current_time,
        weather=weather,
        city=city
    )

# ==================================================
# PREDICTION PAGE
# ==================================================

# ==================================================
# QUICK PREDICTION PAGE
# ==================================================
@app.route("/quick_prediction", methods=["GET","POST"])
def quick_prediction():
@app.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:
        return redirect("/login")

    try:
        temperature_2m_max = float(request.form["temperature_2m_max"])
        temperature_2m_min = float(request.form["temperature_2m_min"])
        apparent_temperature_max = float(request.form["apparent_temperature_max"])
        apparent_temperature_min = float(request.form["apparent_temperature_min"])
        precipitation_sum = float(request.form["precipitation_sum"])
        wind_speed_10m_max = float(request.form["wind_speed_10m_max"])
        wind_gusts_10m_max = float(request.form["wind_gusts_10m_max"])
        weather_code = int(request.form["weather_code"])

        # Create input data
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
        # SEASON DETECTION
        # ==========================================

        month = datetime.now().month

        if month in [3, 4, 5]:
            season = "Summer"
        elif month in [6, 7, 8, 9]:
            season = "Monsoon"
        elif month == 10:
            season = "Post-Monsoon"
        else:
            season = "Winter"

        current_date_display = datetime.now().strftime("%d-%m-%Y")

        # ==========================================
        # AI PREDICTION
        # ==========================================

        result = model.predict(input_data)

        if result[0] == 1:
            prediction_text = "Rain Expected"
        else:
            prediction_text = "No Rain Expected"

        # ==========================================
        # SAVE PREDICTION
        # ==========================================

        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%I:%M %p")

        insert_prediction(
            current_date,
            current_time,
            "Manual Entry",
            temperature_2m_max,
            0,
            wind_speed_10m_max,
            precipitation_sum,
            prediction_text
        )

        # ==========================================
        # GENERATE PDF
        # ==========================================

        generate_pdf(prediction_text)

        # ==========================================
        # RESULT PAGE
        # ==========================================

        return render_template(
            "result.html",
            prediction=prediction_text,
            temperature=temperature_2m_max,
            wind_speed=wind_speed_10m_max,
            rainfall=precipitation_sum,
            season=season,
            current_date=current_date_display
        )

    except Exception as e:
        return f"Error during prediction: {e}"
    if "user_id" not in session:
        return redirect("/login")

    prediction = None
    icon = ""
    temperature = ""
    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M %p")

    if request.method == "POST":

        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])

        if humidity >= 80 and temperature <= 30:
            prediction = "Rain Expected"
            icon = "🌧"

        elif humidity <= 40 and temperature >= 32:
            prediction = "Sunny"
            icon = "☀"

        elif humidity >= 60:
            prediction = "Cloudy"
            icon = "☁"

        else:
            prediction = "Partly Cloudy"
            icon = "⛅"

    return render_template(
        "quick_prediction.html",
        prediction=prediction,
        icon=icon,
        temperature=temperature,
        current_date=current_date,
        current_time=current_time
    )

# ==================================================
# HISTORY PDF
# ==================================================
@app.route("/history_pdf")
def history_pdf():

    if "user_id" not in session:
        return redirect("/login")

    filename = generate_history_pdf()

    return send_file(
        filename,
        as_attachment=True
    )

@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("reports.html")

# ==================================================
# DOWNLOAD PREDICTION PDF
# ==================================================
@app.route("/download_prediction_pdf")
def download_prediction_pdf():

    if "user_id" not in session:
        return redirect("/login")

    pdf_path = os.path.join(
        app.root_path,
        "static",
        "reports",
        "weather_prediction_report.pdf"
    )

    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)

    return "Prediction PDF not found. Please generate a prediction first."

# ==================================================
# EXPORT CSV
# ==================================================
@app.route("/export_csv")
def export_csv():

    if "user_id" not in session:
        return redirect("/login")
    records = get_all_predictions()

    filename = "predictions.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Date",
            "Time",
            "City",
            "Temperature",
            "Humidity",
            "Wind Speed",
            "Rainfall",
            "Prediction"
        ])

        writer.writerows(records)

    return send_file(
        filename,
        as_attachment=True
    )

# Monthly Report
@app.route("/monthly-report")
def monthly_report():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("monthly_report.html")

# ==================================================
# USER REGISTER
# ==================================================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        if register_user(full_name, email, password):

            return render_template(
                "login.html",
                success="Registration Successful. Please Login."
            )

        return render_template(
            "register.html",
            error="Email already exists. Please use another email."
        )

    return render_template("register.html")

# ==================================================
# USER LOGIN
# ==================================================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = login_user(email, password)

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_email"] = user[2]

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid Email or Password"
        )

    return render_template("login.html")

# ==================================================
# ADMIN LOGIN
# ==================================================
@app.route("/admin", methods=["GET", "POST"])
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":

            session["admin_logged_in"] = True

            return redirect("/admin/dashboard")

        return render_template(
            "admin/login.html",
            error="Invalid Username or Password"
        )

    return render_template("admin/login.html")


@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    return render_template(
        "admin/dashboard.html",
        total_predictions=len(records),
        records=records
    )


# ADMIN HISTORY
@app.route("/admin/history")
def admin_history():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    return render_template(
        "admin/history.html",
        records=records
    )

# ==================================================
# ADMIN REPORTS
# ==================================================
@app.route("/admin/reports")
def admin_reports():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    return render_template("admin/reports.html")


# ADMIN USER REPORT
@app.route("/admin/user-report")
def admin_user_report():

    users = get_all_users()

    return render_template(
        "admin/user_report.html",
        users=users,
        total_users=len(users)
    )


# ==================================================
# WEATHER ANALYTICS (Daily / Weekly / Monthly)
# ==================================================
# ==================================================
# MONTHLY AVERAGE TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/monthly-avg")
def monthly_avg_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    monthly_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            month_key = dt.strftime("%B %Y")

            monthly_data[month_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    monthly_stats = []

    for month, temperatures in sorted(
        monthly_data.items()
    ):

        average = sum(temperatures) / len(temperatures)

        monthly_stats.append({
            "month": month,
            "average": round(average, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/monthly_avg_report.html",
        monthly_stats=monthly_stats
    )
# ==================================================
# MONTHLY HIGHEST TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/monthly-highest")
def monthly_highest_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    monthly_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            month_key = dt.strftime("%B %Y")

            monthly_data[month_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    monthly_stats = []

    for month, temperatures in sorted(
        monthly_data.items()
    ):

        highest = max(temperatures)

        monthly_stats.append({
            "month": month,
            "highest": round(highest, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/monthly_highest_report.html",
        monthly_stats=monthly_stats
    )
# ==================================================
# MONTHLY LOWEST TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/monthly-lowest")
def monthly_lowest_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    monthly_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            month_key = dt.strftime("%B %Y")

            monthly_data[month_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    monthly_stats = []

    for month, temperatures in sorted(
        monthly_data.items()
    ):

        lowest = min(temperatures)

        monthly_stats.append({
            "month": month,
            "lowest": round(lowest, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/monthly_lowest_report.html",
        monthly_stats=monthly_stats
    )
# ==================================================
# WEEKLY AVERAGE TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/weekly-avg")
def weekly_avg_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    weekly_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            # ISO year + week
            year, week, _ = dt.isocalendar()

            week_key = f"{year}-W{week:02d}"

            weekly_data[week_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    weekly_stats = []

    for week, temperatures in sorted(
        weekly_data.items()
    ):

        average = sum(temperatures) / len(temperatures)

        weekly_stats.append({
            "week": week,
            "average": round(average, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/weekly_avg_report.html",
        weekly_stats=weekly_stats
    )
# ==================================================
# WEEKLY HIGHEST TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/weekly-highest")
def weekly_highest_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    weekly_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            year, week, _ = dt.isocalendar()

            week_key = f"{year}-W{week:02d}"

            weekly_data[week_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    weekly_stats = []

    for week, temperatures in sorted(
        weekly_data.items()
    ):

        highest = max(temperatures)

        weekly_stats.append({
            "week": week,
            "highest": round(highest, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/weekly_highest_report.html",
        weekly_stats=weekly_stats
    )
# ==================================================
# WEEKLY LOWEST TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/weekly-lowest")
def weekly_lowest_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    weekly_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            year, week, _ = dt.isocalendar()

            week_key = f"{year}-W{week:02d}"

            weekly_data[week_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    weekly_stats = []

    for week, temperatures in sorted(
        weekly_data.items()
    ):

        lowest = min(temperatures)

        weekly_stats.append({
            "week": week,
            "lowest": round(lowest, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/weekly_lowest_report.html",
        weekly_stats=weekly_stats
    )
# ==================================================
# DAILY AVERAGE TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/daily-avg")
def daily_avg_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    daily_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            date_key = dt.strftime("%d-%m-%Y")

            daily_data[date_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    daily_stats = []

    for date, temperatures in sorted(
        daily_data.items(),
        key=lambda x: datetime.strptime(
            x[0],
            "%d-%m-%Y"
        )
    ):

        average = sum(temperatures) / len(temperatures)

        daily_stats.append({
            "date": date,
            "average": round(average, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/daily_avg_report.html",
        daily_stats=daily_stats
    )
# ==================================================
# DAILY HIGHEST TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/daily-highest")
def daily_highest_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    daily_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            date_key = dt.strftime("%d-%m-%Y")

            daily_data[date_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    daily_stats = []

    for date, temperatures in sorted(
        daily_data.items(),
        key=lambda x: datetime.strptime(
            x[0],
            "%d-%m-%Y"
        )
    ):

        highest = max(temperatures)

        daily_stats.append({
            "date": date,
            "highest": round(highest, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/daily_highest_report.html",
        daily_stats=daily_stats
    )
# ==================================================
# DAILY LOWEST TEMPERATURE REPORT
# ==================================================
@app.route("/admin/reports/daily-lowest")
def daily_lowest_report():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    records = get_all_predictions()

    daily_data = defaultdict(list)

    for r in records:

        try:
            date_str = r[1]       # actual format in DB: YYYY-MM-DD
            temperature = float(r[4])

            dt = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            date_key = dt.strftime("%d-%m-%Y")

            daily_data[date_key].append(
                temperature
            )

        except (ValueError, TypeError):
            continue

    daily_stats = []

    for date, temperatures in sorted(
        daily_data.items(),
        key=lambda x: datetime.strptime(
            x[0],
            "%d-%m-%Y"
        )
    ):

        lowest = min(temperatures)

        daily_stats.append({
            "date": date,
            "lowest": round(lowest, 2),
            "records": len(temperatures)
        })

    return render_template(
        "admin/daily_lowest_report.html",
        daily_stats=daily_stats
    )


@app.route("/admin/weather-analytics")
def weather_analytics():

    records = get_all_predictions()
    # records columns: 0 ID, 1 Date, 2 Time, 3 City, 4 Temp, 5 Humidity, 6 Wind, 7 Rain, 8 Prediction

    daily_temps = defaultdict(list)
    monthly_temps = defaultdict(list)
    weekly_temps = defaultdict(list)

    for r in records:
        try:
            date_str = r[1]                     # actual format in DB: YYYY-MM-DD
            temp = float(r[4])
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            continue

        daily_temps[date_str].append(temp)

        month_key = dt.strftime("%B %Y")
        monthly_temps[month_key].append(temp)

        week_key = f"Week {dt.isocalendar()[1]}, {dt.year}"
        weekly_temps[week_key].append(temp)

    # Monthly stats (avg / highest / lowest)
    monthly_stats = {}
    for m, temps in monthly_temps.items():
        monthly_stats[m] = {
            "avg": round(sum(temps) / len(temps), 1),
            "highest": max(temps),
            "lowest": min(temps)
        }

    # Weekly stats (avg / highest / lowest)
    weekly_stats = {}
    for w, temps in weekly_temps.items():
        weekly_stats[w] = {
            "avg": round(sum(temps) / len(temps), 1),
            "highest": max(temps),
            "lowest": min(temps)
        }

    # Daily stats (avg / highest / lowest)
    daily_stats = {}
    for d, temps in sorted(daily_temps.items(), reverse=True):
        daily_stats[d] = {
            "avg": round(sum(temps) / len(temps), 1),
            "highest": max(temps),
            "lowest": min(temps)
        }

    return render_template(
        "admin/weather_analytics.html",
        daily_stats=daily_stats,
        weekly_stats=weekly_stats,
        monthly_stats=monthly_stats
    )

# ADMIN LOGOUT
@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect("/admin/login")

# ==================================================
# HISTORY
# ==================================================
@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    records = get_all_predictions()

    return render_template(
        "history.html",
        records=records
    )

# ==================================================
# AUTO PREDICT (Live Location Weather)
# ==================================================
@app.route("/auto_predict", methods=["POST"])
def auto_predict():

    if "user_id" not in session:
        return jsonify({"error": "Please login first."}), 401

    try:
        data = request.get_json()

        latitude = float(data["latitude"])
        longitude = float(data["longitude"])

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            "&current=temperature_2m,wind_speed_10m"
            "&timezone=auto"
        )

        weather = requests.get(weather_url, timeout=10).json()

        temperature = weather["current"]["temperature_2m"]
        wind_speed = weather["current"]["wind_speed_10m"]

        geo_url = (
            "https://nominatim.openstreetmap.org/reverse"
            f"?lat={latitude}"
            f"&lon={longitude}"
            "&format=jsonv2"
            "&zoom=18"
            "&addressdetails=1"
        )

        geo = requests.get(
            geo_url,
            headers={"User-Agent": "WeatherPredictionApp"}
        ).json()

        address = geo.get("address", {})

        city_name = (
            address.get("city")
            or address.get("town")
            or address.get("municipality")
            or address.get("county")
            or address.get("village")
            or "Unknown"
        )

        state_name = address.get("state", "")

        location = "Karad, Maharashtra"

        result = "☀ No Rain Expected"

        return jsonify({
            "prediction": 0,
            "result": result,
            "location": location,
            "temperature": temperature,
            "wind_speed": wind_speed
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

# ==================================================
# LOGOUT
# ==================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
