import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Important: NEVER hardcode credentials in your code for production!
# Use environment variables or AWS Secrets Manager for sensitive data.
# For demonstration purposes, we'll use os.environ.get()
GMAIL_SENDER_EMAIL = 'lucas.gutknecht@gmail.com'
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', 'your_gmail_app_password') # Or your regular password if 2FA is off and "Less secure app access" is on

subject = "Portfolio Email Notification"
message_body = 'Hello,\n\nThis is a test email from your portfolio website.  If you want to connect reply to this email!\n\nBest regards,\nLucas'
def send_email(email_address):
    """
    Sends an email using Gmail's SMTP server.

    WARNING: This method is generally NOT recommended for production
    applications due to Gmail's sending limits, deliverability concerns,
    and security implications of storing credentials.
    Amazon SES is the preferred AWS service for sending emails.

    Args:
        recipient_email (str): The email address of the recipient.
        subject (str): The subject of the email.
        message_body (str): The plain text body of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        msg = MIMEMultipart("alternative")
        msg['From'] = GMAIL_SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach parts of the email
        part1 = MIMEText(message_body, 'plain')
        # You could add an HTML part here if needed:
        # part2 = MIMEText("<html><body><p>This is <b>HTML</b> body.</p></body></html>", 'html')
        msg.attach(part1)
        # msg.attach(part2)

        # Connect to Gmail's SMTP server
        # For secure connections, always use SSL/TLS (port 465 or 587 with STARTTLS)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)

        print(f"Email successfully sent from {GMAIL_SENDER_EMAIL} to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email via Gmail SMTP: {e}")
        return False