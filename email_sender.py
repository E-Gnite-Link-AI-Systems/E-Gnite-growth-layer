import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    sender_email = "your@gmail.com"
    sender_password = "your_app_password"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print("✅ Email sent to", to_email)
