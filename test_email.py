"""
Quick test script to send a test reminder email
Run this to see what the reminder email looks like
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def send_test_email():
    """Send a test email to see how the reminder looks"""
    
    sender_email = os.getenv("GMAIL_EMAIL")
    sender_password = os.getenv("GMAIL_PASSWORD")
    recipient_email = os.getenv("GMAIL_EMAIL")  # Send to yourself
    
    if not sender_email or not sender_password:
        print("❌ Error: GMAIL_EMAIL or GMAIL_PASSWORD not set in .env file")
        return False
    
    try:
        # Customize these for testing
        gardener_name = "John Doe"  # Change this to test with different names
        task_type = "Front"  # Can be: Front, Back, or Trimming
        scheduled_date = "2026-04-19"
        
        subject = f"🌿 RRBC Garden Care Reminder - Grass Cutting ({task_type})"
        
        body = f"""
Hello {gardener_name},

You are receiving this notification as you have an upcoming schedule for Grass Cutting - {task_type}.

Scheduled Date: {scheduled_date}

Please ensure you complete the task as planned. Thank you for taking care of our garden!

If you have any questions or need assistance, feel free to reach out at 905-621-1034.

Best regards,
George Thuns
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email
        
        message.attach(MIMEText(body, "plain"))
        
        # Send the email
        print(f"📧 Sending test email to {recipient_email}...")
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print("✅ Test email sent successfully!")
        print("\n📋 Email Preview:")
        print("=" * 50)
        print(f"Subject: {subject}")
        print(f"To: {recipient_email}")
        print(f"\n{body}")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        return False

if __name__ == "__main__":
    send_test_email()
