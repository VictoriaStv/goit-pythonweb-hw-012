import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.conf.config import settings


def send_verification_email(to_email: str, username: str, token: str, base_url: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify your email"
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email

    verification_link = f"{base_url}auth/verify-email?token={token}"
    html = f"""
    <html>
      <body>
        <p>Hi, {username}!<br>
           Click the link below to verify your email:<br>
           <a href="{verification_link}">Verify Email</a>
        </p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())

def send_password_reset_email(to_email: str, username: str, token: str, base_url: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Password Reset"
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email

    reset_link = f"{base_url}auth/reset-password?token={token}"
    html = f"""
    <html>
      <body>
        <p>Hi, {username}!<br>
           Click the link below to reset your password:<br>
           <a href="{reset_link}">Reset Password</a>
        </p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
