import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from database import get_connection, get_cursor

load_dotenv()

class EmailReminder:
    def __init__(self):
        self.sender_email = os.getenv("GMAIL_EMAIL", "your_email@gmail.com")
        self.sender_password = os.getenv("GMAIL_PASSWORD", "your_app_password")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, recipient_email, recipient_name, task, scheduled_date):
        """Send email reminder"""
        try:
            subject = f"🌿 RRBC Garden Care Reminder - Grass Cutting ({task})"
            
            body = f"""
Hello {recipient_name},

You are receiving this notification as you have an upcoming schedule for Grass Cutting - {task}.

Scheduled Date: {scheduled_date}

If you are unable to cut as scheduled please trade with someone else on the list or contact our Alternate- Jack Premsler. 

Thank you for taking care of our garden!

Best regards,
RRBC Garden Care Team
            """
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            print(f"✓ Email sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"✗ Failed to send email to {recipient_email}: {str(e)}")
            return False

    def get_gardeners_from_db(self):
        """Get all gardeners from database"""
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            
            cursor.execute("SELECT * FROM gardeners")
            gardeners = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return [dict(row) for row in gardeners]
        except Exception as e:
            print(f"Error fetching gardeners: {str(e)}")
            return []

    def check_and_send_reminders(self):
        """
        Check schedules and send reminders:
        - One day before the scheduled date (scheduled_date - 1)
        - On the scheduled date itself
        """
        gardeners = self.get_gardeners_from_db()
        today = datetime.now().date()
        
        for gardener in gardeners:
            try:
                scheduled_date = datetime.strptime(gardener['date'], '%Y-%m-%d').date()
                day_before = scheduled_date - timedelta(days=1)
                
                # Send reminder one day before scheduled date
                if day_before == today:
                    print(f"📧 Sending reminder to {gardener['name']} (one day before)")
                    self.send_email(
                        gardener['email'],
                        gardener['name'],
                        gardener['task'],
                        gardener['date']
                    )
                
                # Send reminder on the scheduled date itself
                elif scheduled_date == today:
                    print(f"📧 Sending reminder to {gardener['name']} (scheduled date)")
                    self.send_email(
                        gardener['email'],
                        gardener['name'],
                        gardener['task'],
                        gardener['date']
                    )
            
            except Exception as e:
                print(f"Error processing gardener {gardener['name']}: {str(e)}")

def schedule_reminders():
    """Function to be called by scheduler"""
    reminder = EmailReminder()
    reminder.check_and_send_reminders()
