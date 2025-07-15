# formatter/email_template_formatter.py

from datetime import datetime
from pathlib import Path
from rich import print

def generate_email_html(customer_name: str, itinerary: str, total_price: str) -> str:
    date = datetime.now().strftime("%d %b %Y")
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Your Travel Itinerary</title>
</head>
<body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
  <h2>Hello {customer_name},</h2>
  <p>Thank you for booking with us. Below is your travel itinerary:</p>
  <div style="border: 1px solid #ccc; padding: 10px; background: #f9f9f9;">
    {itinerary}
  </div>
  <p><strong>Total Price:</strong> ₹{total_price}</p>
  <p>This email was sent on {date}.</p>
  <p>If you have questions, reply to this message or contact our support team.</p>
  <hr>
  <p style="font-size: 12px; color: #888;">Do not reply to this email if it came from a <code>noreply@</code> address.</p>
</body>
</html>
    """.strip()

def save_email_to_file(html: str, filename: str = "email_preview.html") -> Path:
    path = Path(filename)
    path.write_text(html, encoding="utf-8")
    return path

if __name__ == "__main__":
    customer = input("Customer Name: ").strip()
    itinerary = input("Paste itinerary content (HTML or plain): ").strip()
    price = input("Total Price (e.g. 4599): ").strip()

    html = generate_email_html(customer, itinerary, price)
    file_path = save_email_to_file(html)

    print(f"[green]✓ Email saved to:[/green] {file_path.absolute()}")
