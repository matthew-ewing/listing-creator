import PyPDF2
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader


def generate_download_pdf():
    # Set up the canvas
    pdf = canvas.Canvas("output.pdf", pagesize=landscape(letter))

    # Add the image to the top half of the page
    image_path = "image.jpg"
    with ImageReader(image_path) as image:
        pdf.drawImage(image, 0, 5.5*inch, width=10.5*inch, height=5.5*inch)

    # Add the text to the bottom half of the page
    text = "Click to download"
    link = "https://example.com/download"
    pdf.setFont("Helvetica", 14)
    pdf.setFillColorRGB(0, 0, 255)
    pdf.drawString(2.5*inch, 1*inch, text)

    # Add an underline to the text
    text_width = pdf.stringWidth(text, "Helvetica", 14)
    pdf.setStrokeColorRGB(0, 0, 255)
    pdf.line(2.5*inch, 0.95*inch, 2.5*inch + text_width, 0.95*inch)

    # Add a link to the text
    pdf.linkURL(link, (2.5*inch, 1*inch, 2.5*inch + text_width, 1.15*inch))

    # Save the PDF file
    pdf.save()