from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from database import get_all_predictions


def generate_history_pdf():

    records = get_all_predictions()

    filename = "reports/prediction_history_report.pdf"

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>AI Weather Prediction System</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Prediction History Report", styles["Heading2"])
    )

    data = [[
        "ID",
        "Date",
        "Time",
        "City",
        "Temp",
        "Humidity",
        "Wind",
        "Rainfall",
        "Prediction"
    ]]

    for row in records:
        data.append(list(row))

    table = Table(data)

    table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),colors.darkblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('GRID',(0,0),(-1,-1),1,colors.black),

        ('BACKGROUND',(0,1),(-1,-1),colors.beige),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

        ('BOTTOMPADDING',(0,0),(-1,0),10)

    ]))
    elements.append(table)

    pdf.build(elements)

    return filename