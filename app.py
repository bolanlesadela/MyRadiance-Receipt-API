from flask import Flask, request, send_file
from fpdf import FPDF, XPos, YPos
import io
from datetime import datetime

app = Flask(__name__)

class ReceiptPDF(FPDF):
    def header(self):
        # Cream background for full page
        self.set_fill_color(245, 240, 235)
        self.rect(0, 0, 210, 297, 'F')

        # Top accent bar
        self.set_fill_color(180, 140, 110)
        self.rect(0, 0, 210, 3, 'F')

        # Brand name
        self.add_font("GreatVibes", style="", fname="GreatVibes-Regular.ttf")
        self.set_y(15)
        self.set_font("GreatVibes", size=28)
        self.set_text_color(100, 70, 50)
        self.cell(0, 10, "MyRadiance", align='C',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Tagline
        self.set_font("Helvetica", 'I', 9)
        self.set_text_color(160, 130, 110)
        self.cell(0, 6, "Glow different. Glow radiant.", align='C',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Divider
        self.ln(3)
        self.set_draw_color(180, 140, 110)
        self.set_line_width(0.5)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_fill_color(180, 140, 110)
        self.rect(0, 277, 210, 3, 'F')
        self.set_font("Helvetica", 'I', 8)
        self.set_text_color(160, 130, 110)
        self.cell(0, 10, "Thank you for choosing MyRadiance  |  myradiance.ng",
                  align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)


@app.route('/generate-receipt', methods=['POST'])
def generate_receipt():
    data = request.get_json()
    customer = data.get('customer', 'Customer')
    items = data.get('items', [])

    pdf = ReceiptPDF()
    pdf.add_page()

    # Invoice title
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(160, 130, 110)
    pdf.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # Customer + date info
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(120, 90, 70)
    pdf.cell(0, 7, f"Customer:  {customer}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, f"Date:         {datetime.now().strftime('%B %d, %Y  %H:%M')}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)

    # Table header
    pdf.set_fill_color(180, 140, 110)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", 'B', 10)
    pdf.cell(80, 10, "  PRODUCT", border=0, fill=True)
    pdf.cell(25, 10, "QTY", border=0, fill=True, align='C')
    pdf.cell(40, 10, "PRICE", border=0, fill=True, align='C')
    pdf.cell(40, 10, "SUBTOTAL", border=0, fill=True, align='C')
    pdf.ln()

    # Table rows
    total = 0
    for i, item in enumerate(items):
        subtotal = item['qty'] * item['price']
        total += subtotal
        fill_color = (238, 230, 222) if i % 2 == 0 else (245, 240, 235)
        pdf.set_fill_color(*fill_color)
        pdf.set_text_color(80, 55, 40)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(80, 9, f"  {item['name']}", border=0, fill=True)
        pdf.cell(25, 9, str(item['qty']), border=0, fill=True, align='C')
        pdf.cell(40, 9, f"NGN {item['price']:,}", border=0, fill=True, align='C')
        pdf.cell(40, 9, f"NGN {subtotal:,}", border=0, fill=True, align='C')
        pdf.ln()

    # Bottom divider
    pdf.ln(4)
    pdf.set_draw_color(180, 140, 110)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(5)

    # Total
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(100, 70, 50)
    pdf.cell(0, 10, f"TOTAL:  NGN {total:,}", align='R',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Terms section
    pdf.ln(15)
    pdf.set_draw_color(180, 140, 110)
    pdf.set_line_width(0.3)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", 'B', 9)
    pdf.set_text_color(140, 110, 90)
    pdf.cell(0, 6, "TERMS & CONDITIONS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(160, 130, 110)
    pdf.multi_cell(0, 5,
                   "All sales are final. For damaged or incorrect items, contact us within 48 hours of delivery. MyRadiance is not liable for delays caused by third-party courier services. Thank you for your patronage.")
    pdf.ln(10)

    # Decorative bottom element
    pdf.set_font("Helvetica", 'I', 9)
    pdf.set_text_color(180, 140, 110)
    pdf.cell(0, 6, "* myradiance.ng  |  hello@myradiance.ng  |  @myradiance *",
             align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True,
                     download_name="myradiance-receipt.pdf",
                     mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)