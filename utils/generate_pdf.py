from fpdf import FPDF
from io import BytesIO

def create_pdf(mbti_type, definition):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.set_text_color(106, 13, 173)
    pdf.cell(200, 10, txt="MBTI Result", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, txt=f"Your MBTI type: {mbti_type}\n\nDescription:\n{definition}")

    pdf_output = pdf.output(dest='S').encode('latin1')  # 'S' returns as string
    buffer = BytesIO(pdf_output)
    return buffer
