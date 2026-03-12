from flask import Flask, request, send_file
from fpdf import FPDF, XPos, YPos
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/generate-receipt', methods=['POST'])
def generate_receipt():
    data = request.get_json()

    customer = data.get('customer', 'Customer')
    items = data.get('items', [])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "MyRadiance - Order Receipt", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 10, f"Customer: {customer}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 11)
    pdf.cell(80, 10, "Item", border=1)
    pdf.cell(30, 10, "Qty", border=1, align='C')
    pdf.cell(40, 10, "Price (NGN)", border=1, align='C')
    pdf.cell(40, 10, "Subtotal", border=1, align='C')
    pdf.ln()

    pdf.set_font("Helvetica", size=11)
    total = 0
    for item in items:
        subtotal = item['qty'] * item['price']
        total += subtotal
        pdf.cell(80, 10, item['name'], border=1)
        pdf.cell(30, 10, str(item['qty']), border=1, align='C')
        pdf.cell(40, 10, f"{item['price']:,}", border=1, align='C')
        pdf.cell(40, 10, f"{subtotal:,}", border=1, align='C')
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, f"Total: NGN {total:,}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
    pdf.ln(5)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, "Thank you for shopping with MyRadiance!", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    output_path = "receipt.pdf"
    pdf.output(output_path)

    return send_file(output_path, as_attachment=True, download_name="receipt.pdf")

if __name__ == '__main__':
    app.run(debug=True)