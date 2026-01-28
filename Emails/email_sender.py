import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your SMTP credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "hiresmart.ak@gmail.com"
SENDER_PASSWORD = "fgiz qzny sadq nybv"

def send_email(candidate: dict):
    """
    Sends a confirmation email to the shortlisted candidate with interview time.
    """
    name = candidate.get("name", "Candidate")
    email = candidate.get("email")
    jd_title = candidate.get("job_title", "a job position")
    interview_date = candidate.get("interview_date", "TBD")
    interview_time = candidate.get("interview_time", "TBD")

    if not email:
        print(f"⚠️ Skipping email for {name}, no email provided.")
        return

    subject = f"Interview Confirmation for {jd_title}"
    body = f"""
    Dear {name},

    Congratulations! You have been shortlisted for the position of "{jd_title}".

    📅 Your interview is scheduled for **{interview_date}** at **{interview_time}**.

    Please be available and check your inbox for any updates.

    Best regards,  
    HireSmart AI Team
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent to {name} at {email}")

    except Exception as e:
        print(f"❌ Failed to send email to {name}: {e}")
