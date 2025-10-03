import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

filepath = glob.glob("invoice/*.xlsx")
print("Found files:", filepath)

Path("PDF").mkdir(exist_ok=True)

for filepaths in filepath:
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    filename = Path(filepaths).stem
    invoice_nr = filename.split("-")[0]
    date = filename.split("-")[1]

    pdf.set_font("Times", style="B", size=16)
    pdf.cell(w=100, h=10, txt="QureshiINC", ln=1)
    pdf.set_font("Times", size=12)
    pdf.cell(w=100, h=8, txt="Chungi no 9,multan", ln=1)
    pdf.cell(w=100, h=8, txt="Phone: +92-320-1753593", ln=1)
    pdf.cell(w=100, h=8, txt="Email: hb80128@gmail.com", ln=1)
    pdf.ln(10)

    pdf.set_font("Times", style="B", size=20)
    pdf.cell(w=50, h=8, txt=f"Invoice nr. {invoice_nr}", ln=1)
    pdf.set_font("Times", style="B", size=16)
    pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)
    pdf.ln(10)

    df = pd.read_excel(filepaths)
    
    cols = list(df.columns)
    cols = [item.replace("_", " ").title() for item in cols]

    pdf.set_font("Times", style="B", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=25, h=10, txt=cols[0], border=1, align='C')
    pdf.cell(w=60, h=10, txt=cols[1], border=1, align='C')
    pdf.cell(w=30, h=10, txt=cols[2], border=1, align='C')
    pdf.cell(w=35, h=10, txt=cols[3], border=1, align='C')
    pdf.cell(w=30, h=10, txt=cols[4], border=1, align='C', ln=1)

    total_sum = 0
    for index, row in df.iterrows():
        pdf.set_font("Times", size=9)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(w=25, h=10, txt=str(row["product_id"]), border=1, align='C')
        
        product_name = str(row["product_name"])
        if len(product_name) > 25:
            product_name = product_name[:22] + "..."
        pdf.cell(w=60, h=10, txt=product_name, border=1, align='L')
        
        pdf.cell(w=30, h=10, txt=str(row["amount_purchased"]), border=1, align='C')
        pdf.cell(w=35, h=10, txt=str(row["price_per_unit"]), border=1, align='C')
        pdf.cell(w=30, h=10, txt=str(row["total_price"]), border=1, align='C', ln=1)
        
        total_sum += float(row["total_price"])

    pdf.ln(5)
    pdf.set_font("Times", style="B", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(w=150, h=10, txt="TOTAL:", border=0, align='R')
    pdf.cell(w=30, h=10, txt=f"${total_sum:.2f}", border=1, align='C')
    
    pdf.ln(20)
    pdf.set_font("Times", style="I", size=10)
    pdf.cell(w=0, h=8, txt="Thank you for your business!", align='C', ln=1)
    pdf.cell(w=0, h=8, txt="Payment due within 30 days", align='C')

    output_path = f"PDF/{filename}.pdf"
    print("Saving:", output_path)
    pdf.output(output_path)