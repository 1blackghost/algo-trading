import smtplib
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

def generate_otp():
    """Generate a random OTP (One-Time Password)."""
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

def send_otp(user_email):
    """Send an OTP (One-Time Password) to the specified email address."""
    otp = generate_otp()

    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = config.my_email
    smtp_password = config.app_password
    sender_email = config.my_email

    subject = 'Forgot Password?'
    greeting = 'Hello!,'+user_email+" here is your otp to change your password!\nHave a nice day!"

    # Create a MIMEMultipart object
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = user_email

    # Compose the HTML message
    html_message = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: Arial, sans-serif;
            line-height: 1.5;
            background-color: #f7f7f7;
            padding: 20px;
            text-align: center;
          }}
          .container {{
            background-color: #fff;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            display: inline-block;
            text-align: center;
          }}
          h2 {{
            color: #f00;
            font-size: 28px;
            margin-top: 0;
          }}
          p {{
            color: #555;
            font-size: 20px;
            margin-bottom: 10px;
          }}
          .otp {{
            font-size: 48px;
            font-weight: bold;
            margin-top: 40px;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <img src="https://croniox2.pythonanywhere.com/static/logo.png" alt="Logo" style="width: 150px;">
          <h2>{subject}</h2>
          <p>{greeting}</p>
          <p class="otp">{otp}</p>
        </div>
      </body>
    </html>
    """

    # Create a MIMEText object with the HTML content
    html_content = MIMEText(html_message, "html")

    # Attach the HTML content to the message
    message.attach(html_content)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, user_email, message.as_string())

        print('OTP sent successfully!')
        return otp

    except Exception as e:
        print('An error occurred while sending the OTP:', str(e))
        return None

