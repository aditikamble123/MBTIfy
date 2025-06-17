from fpdf import FPDF
import io

def create_pdf(mbti_type, definition):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=14)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(200, 10, txt="MBTIfy Personality Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Your MBTI Type: {mbti_type}", ln=True)
    pdf.ln(10)

    # Remove non-latin characters from definition to avoid UnicodeEncodeError
    safe_definition = definition.encode("latin1", errors="ignore").decode("latin1")

    pdf.multi_cell(0, 10, safe_definition)

    pdf_output = pdf.output(dest='S').encode('latin1')
    return io.BytesIO(pdf_output)
