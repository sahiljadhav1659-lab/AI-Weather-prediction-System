from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(result):

    filename = "static/reports/weather_prediction_report.pdf"

    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, 760, "Weather Prediction Report")

    c.setFont("Helvetica", 12)

    c.drawString(50, 720, "Project : AI Weather Prediction System")
    c.drawString(50, 700, "Algorithm : Random Forest")
    c.drawString(50, 680, "Prediction : " + result)

    c.drawString(
        50,
        660,
        "Generated On : " + datetime.now().strftime("%d-%m-%Y %I:%M %p")
    )

    c.line(50, 645, 550, 645)

    c.drawString(50, 620, "This report was generated automatically.")

    c.save()

    return filename