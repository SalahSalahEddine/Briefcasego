from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
import datetime
import os
import io
import qrcode
from PIL import Image
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
image_path = os.path.join(MEDIA_DIR,'Capture.jpg')  # static/images/Capture.jpg
"""
Function to generate qrcode
"""
def qrcodex(data):
    qr_img = qrcode.make(data)
    img_buffer = io.BytesIO()
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer

def draw_qr_on_canvas(c, data, x, y, size=100):
    qr_image = qrcodex(data)
    return c.drawInlineImage(Image.open(qr_image), x, y, width=size, height=size)

"""
Function to generate pdf
"""
def generate_isda_confirmation(contract, From, To):
    pdf_path = os.path.join(MEDIA_DIR,'contracts',f"{contract.sender.company_name}_{contract.receiver.company_name}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    margin = 2 * cm
    image_height = 2 * inch
    image_width = width

    c.setFont("Helvetica-Bold", 16)
    c.drawImage(image_path, 0, height - image_height, width=image_width, height=image_height)
    c.setFillColor(colors.white)
    c.drawString(margin, height - margin, f"{contract.contract_type.capitalize()} – Confirmation")
    c.setFont("Helvetica", 10)
    c.drawString(margin, height - margin - 20, "(Under ISDA Master Agreement)")
    y = height - margin - 50

    def draw_section(title, value,font_size=10,color=colors.black,font="Helvetica-Bold"):
        nonlocal y
        c.setFont(font, 10,font_size)
        c.setFillColor(color)
        c.drawString(margin, y, f"{title}")

        c.setFont("Helvetica", 10,font_size)
        c.setFillColor(color)
        c.drawString(margin + 5.5 * cm, y, f"{value}")
        c.setFillColor(colors.black)
        #y -= 15
        y-= font_size + 5

    # Header info
    draw_section("To:", To)
    draw_section("From:", From)
    draw_section("Date:", datetime.datetime.now().date())
    y -= 20
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Transaction Details")
    y -= 20

    # Generate details by contract type
    if contract.contract_type == 'option_call':
        details = [
            ("Trade Date", datetime.datetime.now().date()),
            ("Option Style", contract.option_type),
            ("Option Buyer", To),
            ("Option Seller", From),
            ("Underlying Asset", contract.underlying_asset),
            ("Strike Price", f"{contract.strike_price} $"),
            ("Premium", f"{contract.price} $"),
            ("Expiration Date", contract.expiration_date.strftime("%Y-%m-%d")),
            ("Transferability Clause", contract.third_part),
            ("Settelment Type", contract.settelment_type)
        ]
        for title, value in details:
            draw_section(title, value)
        draw_section("", "")
        draw_section("Sincerely,", "")
        draw_section(f"{From}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        #draw_section(f"{contract.sender_signature}","",font_size=3,color=colors.black,font="Helvetica")
        draw_qr_on_canvas(c, {contract.sender_signature}, x=55, y=400, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Confirmed and Agreed:", "")
        draw_section(f"{To}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:", "",font_size=8,color=colors.black)
        #draw_section(f"{contract.sender_signature}","",font_size=3,color=colors.black,font="Helvetica")
        draw_qr_on_canvas(c, {contract.sender_signature}, x=55, y=300, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Date:", "")
        draw_section(f"[{datetime.datetime.now().date()}]", "")


    elif contract.contract_type == 'interest rate swaps':
        details = [
            ("Trade Date", datetime.datetime.now().date()),
            ("Effective Date", datetime.datetime.now().date()),
            ("Termination Date", f"{contract.duration}"),
            ("Notional Amount", f"{contract.price} $"),
            ("Fixed Rate Payer", From),
            ("Fixed Rate", "3.00% annually"),
            ("Floating Rate Payer", To),
            ("Floating Rate Index", "6M SAIBOR"),
            ("Spread", f"+{contract.spread}%"),
            ("Floating Rate Reset Dates", f"Every {contract.duration} starting {datetime.datetime.now().date()}"),
            ("Payment Dates", "01 Jan and 01 Jul each year"),
            ("Day Count Convention", "Actual/360"),
            ("Governing Law", "New York Law")
        ]
        for title, value in details:
            draw_section(title, value)
        y -= 30
        draw_section("", "")
        draw_section("Sincerely,", "")
        draw_section(f"{From}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        draw_qr_on_canvas(c, {contract.sender_signature}, x=55, y=317, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Confirmed and Agreed:", "")
        draw_section(f"{To}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        draw_qr_on_canvas(c, {contract.receiver_signature}, x=55, y=226, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Date:", "")
        draw_section(f"[{datetime.datetime.now().date()}]", "")
        '''
        # Signature blocks
        y -= 40
        def draw_signature_block(party):
            nonlocal y
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin, y, f"Signature – {party}")
            y -= 15
            c.setFont("Helvetica", 10)
            for label in ["Name:", "Title:", "Signature:", "Date:"]:
                c.drawString(margin + 1 * cm, y, label)
                y -= 15
            y -= 10

        draw_signature_block(From)
        draw_signature_block(To)
        '''
    elif contract.contract_type == 'forward':
        forward_details = [
        ("Trade Date", datetime.datetime.now().date()),
        ("Effective Date", datetime.datetime.now().date()),  # Define in model or calculate
        ("Maturity Date", contract.payment_frequency),    # Define in model or calculate
        ("Buyer", contract.receiver.company_name),
        ("Seller", contract.sender.company_name),
        ("Underlying Asset", contract.underlying_asset),
        ("Quantity", contract.quantity),              # Add to model
        ("Forward Price", f"{contract.forward_price} $"),
        ("Notional Amount", float(contract.forward_price or 0) * float(contract.quantity or 0)),
        ("Settlement Type", contract.settelment_type),
        ("Contract Price", "20 $")
        ]
        for title, value in forward_details:
            draw_section(title, value)
        draw_section("", "")
        draw_section("Sincerely,", "")
        draw_section(f"{From}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        draw_qr_on_canvas(c, {contract.sender_signature}, x=55, y=390, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Confirmed and Agreed:", "")
        draw_section(f"{To}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        draw_qr_on_canvas(c, {contract.receiver_signature}, x=55, y=300, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Date:", "")
        draw_section(f"[{datetime.datetime.now().date()}]", "")

    elif contract.contract_type == 'credit default swaps':
        cds_details = [
        ("Trade Date", datetime.datetime.now().strftime("%Y-%m-%d")),
        ("Buyer of Protection", contract.receiver.company_name),
        ("Seller of Protection", contract.sender.company_name),
        ("Reference Entity", contract.Reference_Entity),
        ("Notional Amount", f"{contract.national_amount} $"),
        ("Premium / Spread", f"{contract.spread} bps per annum"),
        ("Effective Date", datetime.datetime.now().strftime("%Y-%m-%d")),
        ("Maturity Date", contract.payment_frequency.strftime("%Y-%m-%d")),
        ("Payment Frequency", contract.duration),
        ("Settlement Type", contract.settelment_type),
        ("Governing Law", "New York Law")
        ]
        for title, value in cds_details:
            draw_section(title, value)
        y -= 30
        draw_section("", "")
        draw_section("Sincerely,", "")
        draw_section(f"{From}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        draw_qr_on_canvas(c, {contract.sender_signature}, x=55, y=360, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Confirmed and Agreed:", "")
        draw_section(f"{To}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        draw_qr_on_canvas(c, {contract.receiver_signature}, x=55, y=273, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Date:", "")
        draw_section(f"[{datetime.datetime.now().date()}]", "")
        
    elif contract.contract_type == 'naked cds':
        naked_cds_details = [
            ("Buyer of Protection", contract.receiver.company_name),
            ("Seller of Protection", contract.sender.company_name),
            ("Trade Date", datetime.datetime.now().strftime("%Y-%m-%d")),
            ("Maturity Date", contract.payment_frequency.strftime("%Y-%m-%d")),
            ("Notional Amount", f"{contract.national_amount} $"),
            ("Reference Entity", contract.Reference_Entity),
            ("Premium / Spread", f"{contract.spread} bps per annum"),
            ("Payment Frequency", contract.duration),
            ("Governing Law", "New York Law")

        ]
        for title, value in naked_cds_details:
            draw_section(title, value)
        y -= 30
        draw_section("", "")
        draw_section("Sincerely,", "")
        draw_section(f"{From}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        draw_qr_on_canvas(c, {contract.sender_signature}, x=55, y=388, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Confirmed and Agreed:", "")
        draw_section(f"{To}", "",font_size=8,color=colors.black,font="Helvetica")
        draw_section("Signature:","",font_size=8,color=colors.black)
        draw_qr_on_canvas(c, {contract.receiver_signature}, x=55, y=288, size=50)
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("", "")
        draw_section("Date:", "")
        draw_section(f"[{datetime.datetime.now().date()}]", "")
    c.save()
    print("PDF successfully saved:", pdf_path)
