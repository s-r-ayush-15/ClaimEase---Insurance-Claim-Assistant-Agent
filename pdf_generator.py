from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import textwrap

def create_claim_pdf(name, summary_text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x_margin = 50
    y_position = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_margin, y_position, "Insurance Claim Summary")
    c.setFont("Helvetica", 11)
    y_position -= 30

    lines = summary_text.split("\n")
    wrapper = textwrap.TextWrapper(width=90)

    for line in lines:
        if not line.strip():
            y_position -= 12
            continue

        wrapped_lines = wrapper.wrap(line)
        for wline in wrapped_lines:
            c.drawString(x_margin, y_position, wline)
            y_position -= 15
            if y_position < 50:
                c.showPage()
                y_position = height - 50

    c.save()
    buffer.seek(0)
    return buffer
