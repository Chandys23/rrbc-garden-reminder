# 🌿 RRBC Garden Care Reminder App

A web application to manage garden schedules and send automated email reminders to gardeners. Built with FastAPI (Python) backend and an interactive HTML/JavaScript frontend.

## Features

✅ **Manage Gardener Schedules** - Add, edit, and delete garden care schedules  
✅ **Editable Table Interface** - User-friendly table with inline editing  
✅ **Automated Email Reminders** - Send reminders via Gmail SMTP  
✅ **Smart Scheduling** - Reminders sent automatically:
  - One day before the scheduled date
  - On the scheduled date itself
  - Works for any day of the week (not limited to specific days)
✅ **Local Phase-1** - Runs entirely on your local machine  
✅ **Responsive Design** - Works on desktop and mobile

## System Requirements

- Python 3.8 or higher
- Gmail account (for sending email reminders)
- Windows/Mac/Linux

## Administration

This schedule and reminder system is managed by **two administrators**. The management team ensures timely updates to the garden care schedule and deployment of reminder notifications to team members.

## Installation & Setup

### Step 1: Clone/Extract the Project

The project is already in your workspace:
```
e:\Chandan\Python\VS Code\RRBC Garden care Reminder App
```

### Step 2: Set Up Python Environment

1. Open PowerShell or Command Prompt in the project directory
2. Create a virtual environment:
```powershell
python -m venv venv
```

3. Activate the virtual environment:

**Option A - Windows Command Prompt (Recommended):**
```cmd
venv\Scripts\activate.bat
```

**Option B - Windows PowerShell:**
```powershell
# If you get a script execution policy error, use one of these:

# Method 1: Use the batch file instead (easiest)
.\venv\Scripts\Activate.bat

# Method 2: Temporarily bypass execution policy for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1

# Method 3: Permanently change execution policy (not recommended)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Gmail SMTP

To send emails, you need to set up Gmail credentials:

1. **Enable 2-Factor Authentication** on your Google account:
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate an App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password

3. **Create `.env` file** in the project root:
   ```
   GMAIL_EMAIL=your_email@gmail.com
   GMAIL_PASSWORD=your_app_password_here
   ```

**Note:** Replace `your_email@gmail.com` and `your_app_password_here` with your actual values.

### Step 5: Run the Application

From the project root directory (with venv activated):

```powershell
python backend/main.py
```

You should see:
```
✓ Database initialized
✓ Reminder scheduler started
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 6: Access the Application

Open your web browser and go to:
```
http://127.0.0.1:8000
```

## Usage

### Adding a Schedule

1. Fill in the form at the top:
   - **Date**: Select the date (usually a Saturday for grass cutting)
   - **Gardener Name**: Enter the gardener's name
   - **Task Type**: Choose from Front, Back, or Trimming
   - **Email**: Enter the gardener's email
   - **Mobile**: Enter the gardener's phone number
2. Click **"Add Schedule"** button

### Editing a Schedule

1. Find the schedule in the table
2. Click the **"Edit"** button
3. Modify the details in the form
4. Click **"Save Changes"**

### Deleting a Schedule

1. Find the schedule in the table
2. Click the **"Delete"** button
3. Confirm the deletion

## How Email Reminders Work

The app automatically sends reminders based on the scheduled date:

**Example:** If you schedule grass cutting for Saturday, May 4th:
- **Friday, May 3rd at Noon**: Email sent reminding about Saturday task
- **Saturday, May 4th at 9 AM**: Email sent on the morning of the task

The reminders are sent automatically every hour by the background scheduler.

## Database

- **Location**: `gardeners.db` in the project root
- **Type**: SQLite (serverless, no setup needed)
- **Tables**: `gardeners` table stores all schedule information

## Project Structure

```
RRBC Garden care Reminder App/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLite database setup
│   └── reminders.py         # Email reminder scheduler
├── frontend/
│   └── index.html           # Web interface
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Your actual Gmail credentials (DO NOT COMMIT)
└── gardeners.db            # SQLite database (auto-created)
```

## API Endpoints

### Get all schedules
```
GET /api/gardeners
```

### Get specific schedule
```
GET /api/gardeners/{id}
```

### Create new schedule
```
POST /api/gardeners
Body: {
  "date": "2026-05-04",
  "name": "John Doe",
  "task": "Front",
  "email": "john@example.com",
  "mobile": "123-456-7890"
}
```

### Update schedule
```
PUT /api/gardeners/{id}
Body: { same as POST }
```

### Delete schedule
```
DELETE /api/gardeners/{id}
```

## Troubleshooting

### PowerShell Script Execution Policy Error
If you get: `cannot be loaded because running scripts is disabled on this system`

**Solution:** Use Command Prompt instead:
```cmd
# Open Command Prompt (not PowerShell)
cd e:\Chandan\Python\VS Code\RRBC Garden care Reminder App
venv\Scripts\activate.bat
python backend/main.py
```

Or if you prefer PowerShell, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```
Then activate:
```powershell
.\venv\Scripts\Activate.ps1
```

### "Module not found" error
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Email not sending
- Check that `.env` file exists with correct Gmail credentials
- Verify Gmail account has 2-Factor Authentication enabled
- Verify that you generated an App Password (not regular password)
- Check that the GMAIL_EMAIL matches the account used

### Port 8000 already in use
- The app is probably still running from a previous session
- Kill the process or use a different port by modifying `main.py`

### Database issues
- Delete `gardeners.db` and restart the app
- The database will be automatically recreated

## Next Steps (Phase 2 - External Hosting)

To deploy this to external hosting:

1. **Database Migration**: Move from SQLite to PostgreSQL/MySQL
2. **Hosting Options**:
   - Heroku (free tier available)
   - PythonAnywhere
   - AWS/DigitalOcean
   - Azure App Service
3. **Email Service**: Consider SendGrid or Mailgun for better reliability
4. **Authentication**: Add admin login for Phase 2

## Security Notes

⚠️ **Important for Production:**
- Never commit `.env` file to version control (already in `.gitignore`)
- Use environment variables for all sensitive data
- Consider using a proper email service provider
- Add authentication for admin access in Phase 2
- Use HTTPS in production

## Support & Documentation

For more information on the technologies used:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)

## License

This project is for personal use within RRBC organization.

---

**Created**: April 2026  
**Version**: 1.0 (Phase 1 - Local)  
**Ready for Phase 2 External Hosting**
