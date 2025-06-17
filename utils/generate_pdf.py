from fpdf import FPDF
import io
import os

def create_pdf(mbti_type, definition):
    pdf = FPDF()
    pdf.add_page()

    # Set Unicode font
    font_path = os.path.join("utils", "DejaVuSans.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError("Font file 'DejaVuSans.ttf' not found in utils/ directory.")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", "", 14)

    pdf.set_text_color(40, 40, 40)
    pdf.cell(200, 10, txt="🧠 MBTIfy Personality Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(200, 10, txt=f"Your MBTI Type: {mbti_type}", ln=True)
    pdf.ln(10)

    # Handle line wrapping for long text
    pdf.multi_cell(0, 10, definition)

    pdf_output = pdf.output(dest='S').encode('latin1', errors='replace')  # replace unsupported
    return io.BytesIO(pdf_output)
