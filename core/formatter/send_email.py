# formatter/send_email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rich import print

def send_email(recipient_email, subject, html_body, sender_email, app_password, plain_text="This is a travel itinerary."):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        print(f"[green]✓ Email sent to {recipient_email}[/green]")
        return True

    except Exception as e:
        print(f"[red]✗ Failed to send email: {e}[/red]")
        return False
