
# Email bhejne ke liye required Python libraries


import smtplib                           # SMTP protocol ke liye
from email.mime.text import MIMEText     # Email body (plain text)
from email.mime.multipart import MIMEMultipart  # Email structure (subject + body)


# EMAIL CONFIGURATION
#  Production me ye values .env file se aani chahiye


SMTP_SERVER = "smtp.gmail.com"       # Gmail SMTP server
SMTP_PORT = 587                      # TLS secure port

SENDER_EMAIL = "your_email@gmail.com"        # OTP / reset link bhejne wala email
SENDER_PASSWORD = "your_app_password"        # Gmail App Password (NOT normal password)



# COMMON EMAIL SENDER FUNCTION

def send_email(receiver_email: str, subject: str, body: str):
    """
    Ye generic function hai jo kisi bhi type ka email bhej sakta hai

    receiver_email → jisko email bhejna hai
    subject        → email ka subject
    body           → email ka content
    """


    # Email message object
  
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Email body attach
    msg.attach(MIMEText(body, "plain"))

    try:
        
        # SMTP server se connect
   
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure TLS connection

        # Gmail login (App Password)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Email send
        server.sendmail(
            SENDER_EMAIL,
            receiver_email,
            msg.as_string()
        )

        # Server connection close
        server.quit()

        print(" Email sent successfully")

    except Exception as e:
        print(" Failed to send email")
        print(e)
        raise


# OTP EMAIL FUNCTION (REGISTER / FORGOT PASSWORD)

def send_otp_email(receiver_email: str, otp: str):
    """
    Ye function user ke email par OTP bhejta hai

    receiver_email → jisko OTP bhejna hai
    otp            → 6 digit OTP
    """

    subject = "Your OTP for Secure Notes"

    body = f"""
Hello,

Your One-Time Password (OTP) is:

    OTP: {otp}

This OTP is valid for 10 minutes only.

If you did not request this, please ignore this email.

Thanks & Regards,
Secure Notes Team
"""

    # Common email sender function call
    send_email(receiver_email, subject, body)


# PASSWORD RESET EMAIL FUNCTION

def send_reset_password_email(receiver_email: str, reset_token: str):
    """
    Ye function forgot password ke liye reset link bhejta hai

    receiver_email → user ka email
    reset_token   → secure reset token
    """

    # Frontend reset password page ka URL
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"

    subject = "Reset Your Secure Notes Password"

    body = f"""
Hello,

You requested to reset your password.

Click the link below to reset your password:

{reset_link}

This link is valid for 15 minutes only.

If you did not request this, please ignore this email.

Thanks & Regards,
Secure Notes Team
"""

    send_email(receiver_email, subject, body)
