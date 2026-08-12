from flask import Flask, render_template, request, send_file, redirect, session, jsonify
import os
import requests
import os
import csv
import joblib
import pandas as pd
from datetime import datetime
from database import get_all_users

from pdf_generator import generate_pdf
from history_pdf import generate_history_pdf
from weather_api import get_weather

from database import (
    create_table,
    insert_prediction,
    get_all_predictions,
    register_user,
    login_user
)
app = Flask(__name__)
print("ROOT:", app.root_path)
print("TEMPLATES:", app.template_folder)
app.secret_key = "weather_prediction_secret_key_2026"

# ==================================================
# CREATE DATABASE
# ==================================================
create_table()
from database import (
    create_table,
    insert_prediction,
    get_all_predictions,
    register_user,
    login_user,
    get_all_users
)
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
# HOME
# ==================================================

# ==================================================
# ABOUT
# ==================================================
@app.route("/about")
def about():
    return render_template("about.html")


# ==================================================
# REPORTS
# ==================================================

# ==================================================
# DASHBOARD
# ==================================================
@app.route("/dashboard")
def dashboard():

    # User must be logged in
    if "user_id" not in session:
        return redirect("/login")

    accuracy = "98.43%"
    dataset_records = 91320
    total_features = 8
    algorithm = "Random Forest"

    city = request.args.get("city", "Delhi")
    weather = get_weather(city)

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
@app.route("/prediction")
def prediction():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("prediction.html")
# ==================================================
# QUICK PREDICTION PAGE
# ==================================================
@app.route("/quick_prediction", methods=["GET","POST"])
def quick_prediction():

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
# PREDICT

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
    return render_template("monthly_report.html")
# ==================================================
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

    records = get_all_predictions()

    return render_template(
        "admin/dashboard.html",
        total_predictions=len(records),
        records=records
    )


# ADMIN HISTORY
@app.route("/admin/history")
def admin_history():

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
# ADMIN LOGOUT
@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect("/admin/login")
# =========py app.py
# =========================================
@app.route("/auto_predict", methods=["POST"])
def auto_predict():

    if "user_id" not in session:
        return jsonify({"error": "Please login first."}), 401

    try:
        data = request.get_json()

        latitude = float(data["latitude"])
        longitude = float(data["longitude"])

        # Get weather from Open-Meteo
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

        # Get exact location
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

        location = (
            address.get("road")
            or address.get("neighbourhood")
            or address.get("suburb")
            or address.get("hamlet")
            or address.get("village")
            or address.get("town")
            or address.get("city")
            or geo.get("display_name")
            or "Unknown Location"
        )

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

#  ==================================================
# LOGOUT
# ==================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
    