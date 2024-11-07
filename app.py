from flask import Flask
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Load recruiter emails from the provided list
def load_emails():
    with open('ListEntreprises.txt', 'r') as file:
        return [line.strip() for line in file if '@' in line]

# Send email function
def send_email(to_email, subject, body, resume_path):
    # Email account credentials from environment variables
    sender_email = os.getenv("SENDER_EMAIL")  # Set this in your .env file
    sender_password = os.getenv("SENDER_PASSWORD")  # Set this in your .env file

    if not sender_email or not sender_password:
        print("Email credentials are missing from environment variables.")
        return

    # Email setup
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach resume
    with open(resume_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name="Resume.pdf")
        part['Content-Disposition'] = 'attachment; filename="Resume.pdf"'
        msg.attach(part)

    # Connect to SMTP server and send email
    try:
        smtp_server = os.getenv("SMTP_SERVER")  # Set SMTP server in your .env file
        smtp_port = int(os.getenv("SMTP_PORT", 587))  # Default to port 587 if not set

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Function to send emails to a batch of recruiters
def send_batch_emails():
    emails = load_emails()
    batch_size = 500
    resume_path = "AmineResu.pdf"  # Path to your resume
    subject = "Job Application"
    body = "Dear Recruiter,\n\nPlease find attached my resume and motivation letter.\n\nBest regards,\nAmine Zeta"

    for email in emails[:batch_size]:
        send_email(email, subject, body, resume_path)
    print("Batch of 500 emails sent.")

@app.route("/send-emails")
def send_emails():
    send_batch_emails()
    return "Emails Sent!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
