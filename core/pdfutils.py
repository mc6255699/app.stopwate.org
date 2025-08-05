import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER


#This Generates the stamp page
def generate_cover_page(invoice):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import LETTER
    from io import BytesIO

    # Convert model instance to dict
    data = {
        'Owner': invoice.owner.username if invoice.owner else 'N/A',
        'Code': invoice.code,
        'Note': invoice.note,
        'Uploaded At': invoice.uploaded_at.strftime('%Y-%m-%d %H:%M'),
    }

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    textobject = c.beginText(50, 750)
    textobject.setFont("Helvetica", 12)

    for key, value in data.items():
        textobject.textLine(f"{key}: {value}")

    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


#this function adds the cover page
def merge_cover_with_invoice(cover_pdf, uploaded_pdf):
    writer = PdfWriter()

    # cover_pdf is already a BytesIO object
    cover_reader = PdfReader(cover_pdf)
    uploaded_reader = PdfReader(uploaded_pdf)

    for page in cover_reader.pages:
        writer.add_page(page)

    for page in uploaded_reader.pages:
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output


#this removes the cover page for a restamp
def remove_cover_page(pdf_file):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    # Skip the first page (cover page)
    for page in reader.pages[1:]:
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output