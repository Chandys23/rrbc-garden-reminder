# 🌿 RRBC Garden Care Reminder App - Complete Technical Guide

## Table of Contents
1. [Project Structure](#project-structure)
2. [Technology Stack](#technology-stack)
3. [How the App Works](#how-the-app-works)
4. [File Breakdown](#file-breakdown)
5. [Data Flow](#data-flow)
6. [API Endpoints](#api-endpoints)
7. [Frontend Logic](#frontend-logic)
8. [Email Reminder System](#email-reminder-system)
9. [Database Schema](#database-schema)

---

## Project Structure

```
RRBC Garden care Reminder App/
├── backend/                    # Python backend services
│   ├── main.py                 # FastAPI application & API routes
│   ├── database.py             # SQLite database initialization
│   └── reminders.py            # Email reminder scheduler
├── frontend/                   # Web interface
│   └── index.html              # Single-page application (HTML+CSS+JS)
├── requirements.txt            # Python dependencies
├── .env                        # Gmail credentials (YOUR SECRETS)
├── .env.example                # Template for .env
├── .gitignore                  # Git ignore rules
├── gardeners.db                # SQLite database (auto-created)
├── test_email.py               # Email testing script
└── README.md                   # Documentation
```

---

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework for building APIs
- **Uvicorn** - ASGI server (runs the application)
- **SQLite** - Local file-based database (no installation needed)
- **SQLAlchemy** - ORM for database operations
- **APScheduler** - Background job scheduler for email reminders
- **Python-dotenv** - Load environment variables from .env file
- **smtplib** - Built-in Python library for sending emails via Gmail

### Frontend
- **HTML/CSS/JavaScript** - Vanilla (no frameworks like React/Vue)
- **Fetch API** - For communicating with backend
- **Local Storage** - Client-side state management

### External Services
- **Gmail SMTP** - For email delivery

---

## How the App Works

### High-Level Flow

```
User Input (Web Browser)
         ↓
    Frontend (index.html)
         ↓
    FastAPI Backend (main.py)
         ↓
    Database (gardeners.db)
         ↓
    Schedule Checker (reminders.py - runs every hour)
         ↓
    Gmail SMTP
         ↓
    Gardener's Email
```

### User Journey

1. **User opens browser** → `http://127.0.0.1:8000`
2. **Frontend loads** → Beautiful UI with form and table
3. **User enters schedule** → Name, Date, Task, Email, Mobile
4. **Frontend sends request** → POST to `/api/gardeners`
5. **Backend receives** → Validates data and saves to database
6. **Table updates** → Shows all schedules
7. **Background scheduler** → Every hour checks for reminders
8. **Saturday tasks found** → Sends Friday 5 PM & Saturday 9 AM emails

---

## File Breakdown

### 1. **backend/main.py** - FastAPI Application

**Purpose:** Creates the web server and handles all API requests

**Key Components:**

```python
# Initialize FastAPI app
app = FastAPI(title="RRBC Garden Reminder API")

# CORS middleware - allows frontend to talk to backend
app.add_middleware(CORSMiddleware, ...)

# Database initialization on startup
@app.on_event("startup")
def startup_event():
    init_db()  # Create tables if they don't exist
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_reminders, 'interval', hours=1)
    scheduler.start()
```

**Logic Flow:**
```
Request comes in
    ↓
Route handler processes request
    ↓
Database operation (CRUD)
    ↓
Response sent back to frontend
```

**Pydantic Models** (Data validation):
```python
class Gardener(BaseModel):
    date: str              # Format: YYYY-MM-DD
    name: str              # Gardener's name
    task: str              # "Front", "Back", or "Trimming"
    email: str             # Email address
    mobile: str            # Phone number
```

---

### 2. **backend/database.py** - Database Setup

**Purpose:** Initialize SQLite database and create tables

**How it works:**

```python
def init_db():
    # Creates "gardeners" table if it doesn't exist
    # Table structure:
    
    CREATE TABLE gardeners (
        id INTEGER PRIMARY KEY,           # Unique ID (auto-increment)
        date TEXT NOT NULL,               # Schedule date (YYYY-MM-DD)
        name TEXT NOT NULL,               # Gardener name
        task TEXT NOT NULL,               # Task type (Front/Back/Trimming)
        email TEXT NOT NULL,              # Email address
        mobile TEXT NOT NULL,             # Phone number
        created_at TIMESTAMP              # When record was created
    )
```

**Key Functions:**
- `get_connection()` - Opens a connection to the database
- `init_db()` - Creates the table structure

---

### 3. **backend/reminders.py** - Email Scheduler

**Purpose:** Check schedules and send automatic email reminders

**Logic Flow:**

```python
def check_and_send_reminders():
    # Get all gardeners from database
    gardeners = get all records from gardeners table
    
    # Get today's date and current hour
    today = April 17, 2026 (example)
    current_hour = 17 (5 PM)
    
    # Loop through each gardener
    For each gardener:
        scheduled_date = Parse gardener's date
        
        # Check if schedule is for Saturday
        if scheduled_date is a SATURDAY:
            
            # Friday 5 PM reminder
            if today is FRIDAY and current_hour is 5 PM:
                Send email to gardener
            
            # Saturday 9 AM reminder
            if today is SATURDAY and current_hour is 9 AM:
                Send email to gardener
```

**Email Structure:**

```
Subject: 🌿 RRBC Garden Care Reminder - Grass Cutting (Front)

Body:
Hello [Gardener Name],

You are receiving this notification as you have an upcoming 
schedule for Grass Cutting - [Front/Back/Trimming].

Scheduled Date: [Date]

Please ensure you complete the task as planned. 
Thank you for taking care of our garden!

Best regards,
RRBC Garden Care Team
```

**Key Function:**
```python
def send_email(recipient_email, recipient_name, task, scheduled_date):
    # Connects to Gmail SMTP server
    # Authenticates with credentials from .env
    # Sends formatted email
    # Logs success or failure
```

---

### 4. **frontend/index.html** - Web Interface

**Purpose:** User-facing interface for managing schedules

**Components:**

#### a) **HTML Structure**
```html
<header>           <!-- Title and branding -->
<stats>            <!-- Total schedules, upcoming count -->
<form>             <!-- Add/Edit schedule form -->
<table>            <!-- Display all schedules -->
```

#### b) **CSS Styling**
```css
- Gradient purple background
- White container with rounded corners
- Responsive grid layout
- Color-coded buttons (green=save, red=delete, blue=edit)
- Hover effects for interactivity
```

#### c) **JavaScript Logic**

**When page loads:**
```javascript
1. loadSchedules() - Fetch all schedules from API
2. updateStats() - Calculate total & upcoming counts
3. Display data in table
```

**When user clicks "Add Schedule":**
```javascript
1. Get form values (date, name, task, email, mobile)
2. Validate all fields are filled
3. Send POST request to /api/gardeners
4. If success:
   - Show success message
   - Clear form
   - Reload table
5. If error:
   - Show error message
```

**When user clicks "Edit":**
```javascript
1. Fetch full details for that schedule
2. Populate form with existing values
3. Change button text from "Add" to "Save Changes"
4. Show "Cancel" button
5. Save editing ID for later update
```

**When user clicks "Save Changes":**
```javascript
1. Send PUT request to /api/gardeners/{id}
2. Update database record
3. Reset form
4. Reload table
```

**When user clicks "Delete":**
```javascript
1. Ask confirmation: "Are you sure?"
2. If confirmed:
   - Send DELETE request to /api/gardeners/{id}
   - Remove from database
   - Refresh table
```

---

## Data Flow

### Adding a New Schedule

```
Frontend Form Input
    ↓
    date: "2026-04-19"
    name: "John Doe"
    task: "Front"
    email: "john@example.com"
    mobile: "905-621-1034"
    ↓
JavaScript Validation (All filled?)
    ↓
Fetch Request: POST /api/gardeners
    ↓
FastAPI Route Handler
    ↓
Pydantic Validation (Correct format?)
    ↓
SQLite INSERT
    INSERT INTO gardeners (date, name, task, email, mobile)
    VALUES ('2026-04-19', 'John Doe', 'Front', 'john@example.com', '905-621-1034')
    ↓
Database Returns ID = 1
    ↓
Response: {id: 1, message: "Gardener added successfully"}
    ↓
Frontend Receives Response
    ↓
Show Success Message
    ↓
Clear Form & Reload Table
```

### Background Email Reminder Process

```
APScheduler triggers every hour
    ↓
schedule_reminders() function runs
    ↓
Query database: SELECT * FROM gardeners
    ↓
For each schedule:
    Get scheduled_date
    
    Check: Is it a Saturday?
    ├─ NO → Skip to next gardener
    └─ YES ↓
        
        Check: Is today Friday?
        └─ YES ↓
            Check: Is it 5 PM (17:00)?
            └─ YES ↓
                Send email to gardener
        
        Check: Is today Saturday?
        └─ YES ↓
            Check: Is it 9 AM (08:00)?
            └─ YES ↓
                Send email to gardener
    ↓
Gmail SMTP sends email
    ↓
Email arrives in gardener's inbox
```

---

## API Endpoints

### 1. **GET /api/gardeners**
**Purpose:** Fetch all schedules

**Request:** No body needed
```
GET http://127.0.0.1:8000/api/gardeners
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "date": "2026-04-19",
    "name": "John Doe",
    "task": "Front",
    "email": "john@example.com",
    "mobile": "905-621-1034",
    "created_at": "2026-04-17T10:30:00"
  }
]
```

---

### 2. **GET /api/gardeners/{id}**
**Purpose:** Fetch a specific schedule

**Request:**
```
GET http://127.0.0.1:8000/api/gardeners/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "date": "2026-04-19",
  "name": "John Doe",
  "task": "Front",
  "email": "john@example.com",
  "mobile": "905-621-1034",
  "created_at": "2026-04-17T10:30:00"
}
```

---

### 3. **POST /api/gardeners**
**Purpose:** Create a new schedule

**Request:**
```
POST http://127.0.0.1:8000/api/gardeners
Content-Type: application/json

{
  "date": "2026-04-19",
  "name": "John Doe",
  "task": "Front",
  "email": "john@example.com",
  "mobile": "905-621-1034"
}
```

**Backend Processing:**
```python
1. Receive JSON payload
2. Create Gardener object (Pydantic validates)
3. Check date format: YYYY-MM-DD
4. Execute SQL: INSERT INTO gardeners...
5. Get back ID (auto-increment)
6. Return success response
```

**Response (200 OK):**
```json
{
  "id": 1,
  "message": "Gardener added successfully"
}
```

---

### 4. **PUT /api/gardeners/{id}**
**Purpose:** Update an existing schedule

**Request:**
```
PUT http://127.0.0.1:8000/api/gardeners/1
Content-Type: application/json

{
  "date": "2026-04-26",
  "name": "John Doe",
  "task": "Back",
  "email": "john@example.com",
  "mobile": "905-621-1034"
}
```

**Backend Processing:**
```python
1. Receive JSON payload and ID
2. Validate all fields
3. Execute SQL: UPDATE gardeners SET ... WHERE id=1
4. Return success message
```

**Response (200 OK):**
```json
{
  "message": "Gardener updated successfully"
}
```

---

### 5. **DELETE /api/gardeners/{id}**
**Purpose:** Delete a schedule

**Request:**
```
DELETE http://127.0.0.1:8000/api/gardeners/1
```

**Backend Processing:**
```python
1. Receive ID
2. Execute SQL: DELETE FROM gardeners WHERE id=1
3. Check if row was deleted (rowcount > 0)
4. Return success/error message
```

**Response (200 OK):**
```json
{
  "message": "Gardener deleted successfully"
}
```

---

## Frontend Logic

### JavaScript Functions

#### 1. **loadSchedules()**
```javascript
Fetches POST request to /api/gardeners
Gets JSON response with all schedules

If empty:
    Show "No schedules yet" message
Else:
    Loop through each schedule
    Create HTML table rows
    Add Edit and Delete buttons
    Insert into page
```

#### 2. **addSchedule()**
```javascript
Get form values:
    date: document.getElementById('date').value
    name: document.getElementById('name').value
    task: document.getElementById('task').value
    email: document.getElementById('email').value
    mobile: document.getElementById('mobile').value

Validate:
    If any field is empty → Show error

If editing (editingId exists):
    POST to /api/gardeners/{editingId} (PUT request)
Else:
    POST to /api/gardeners (POST request)

Parse response:
    If response.ok → Show success, refresh
    Else → Show error
```

#### 3. **editSchedule(id)**
```javascript
Fetch /api/gardeners/{id}
Get schedule details

Fill form fields:
    document.getElementById('date').value = schedule.date
    document.getElementById('name').value = schedule.name
    etc.

Change UI:
    formTitle = "Edit Garden Schedule"
    submitBtn = "Save Changes"
    Show cancelBtn

Set: editingId = id

Scroll to form
```

#### 4. **deleteSchedule(id)**
```javascript
Show confirmation dialog:
    "Are you sure?"

If confirmed:
    Fetch DELETE /api/gardeners/{id}
    If success → Show message, refresh table
    If error → Show error
```

#### 5. **updateStats()**
```javascript
Count total schedules in table
Count schedules within next 7 days

Update display:
    document.getElementById('totalCount').textContent = count
    document.getElementById('upcomingCount').textContent = upcomingCount
```

---

## Email Reminder System

### ✅ Updated Scheduling Architecture (Deployed)

```
FastAPI App Starts
    ↓
APScheduler initializes
    ↓
Creates job: check_and_send_reminders()
    ↓
Runs every 1 hour indefinitely
    ↓
Each hour check:
    - Get all gardeners from database
    - Check today's date
    - Compare with scheduled dates
    - Send emails if conditions match
```

### Updated Reminder Logic ✅

**Sends reminders for ANY scheduled date** (not just Saturdays):
- Reminder 1: One day BEFORE scheduled date
- Reminder 2: ON the scheduled date itself

```python
def check_and_send_reminders():
    today = datetime.now().date()
    gardeners = get_all_gardeners_from_db()
    
    for gardener in gardeners:
        scheduled_date = datetime.strptime(gardener['date'], '%Y-%m-%d').date()
        day_before = scheduled_date - timedelta(days=1)
        
        # Send reminder ONE DAY BEFORE
        if day_before == today:
            print(f"📧 Sending reminder to {gardener['name']} (one day before)")
            send_email(
                gardener['email'],
                gardener['name'],
                gardener['task'],
                gardener['date']
            )
        
        # Send reminder ON THE SCHEDULED DATE
        elif scheduled_date == today:
            print(f"📧 Sending reminder to {gardener['name']} (scheduled date)")
            send_email(
                gardener['email'],
                gardener['name'],
                gardener['task'],
                gardener['date']
            )
```

### Example Timeline

| Day | Event | Reminder |
|-----|-------|----------|
| Mon 4/24 | (no action) | - |
| **Tue 4/25** | **SCHEDULED DATE** | ✉️ Email sent |
| Wed 4/26 | (no action) | - |
| Thu 4/27 | (no action) | - |
| Fri 4/28 | (no action) | - |
| **Sat 4/29** | **SCHEDULED DATE** | ✉️ Email sent |
| **Fri 5/2** | (one day before 5/3) | ✉️ Email sent |
| **Sat 5/3** | **SCHEDULED DATE** | ✉️ Email sent |

### Email Template

```
From: your_email@gmail.com
To: gardener@example.com
Subject: 🌿 RRBC Garden Care Reminder - Grass Cutting (Front)

---

Hello John,

You are receiving this notification as you have an upcoming 
schedule for Grass Cutting - Front.

Scheduled Date: 2026-04-25

Please ensure you complete the task as planned. Thank you for 
taking care of our garden!

Best regards,
RRBC Garden Care Team
```

### How It Works

1. **Process always running** - APScheduler keeps scheduler active
2. **Hourly checks** - Every hour checks for reminders
3. **Date-based logic** - Compares database dates with today's date
4. **Persistent storage** - Schedules saved in gardeners.db
5. **Gmail credentials** - Loaded from .env file
6. **SMTP connection** - Secure connection to Gmail servers

### Scheduler Status in Logs

When app deploys, you'll see:
```
✓ Database initialized
✓ Reminder scheduler started (runs every 1 hour)
```

Each hour (automatically):
```
📧 Sending reminder to John (one day before)
✓ Email sent to john@example.com
```

---

## Database Schema

### gardeners Table

```sql
CREATE TABLE gardeners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,           -- YYYY-MM-DD format
    name TEXT NOT NULL,           -- Gardener's name
    task TEXT NOT NULL,           -- "Front", "Back", or "Trimming"
    email TEXT NOT NULL,          -- Email address for reminders
    mobile TEXT NOT NULL,         -- Phone number
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Sample Data

```
id | date       | name   | task     | email              | mobile
---|------------|--------|----------|--------------------|-----------
1  | 2026-04-25 | John   | Front    | john@example.com   | 905-621-1034
2  | 2026-04-30 | Sarah  | Back     | sarah@example.com  | 416-555-2019
3  | 2026-05-05 | Mike   | Trimming | mike@example.com   | 647-555-3045
```

---

## Environment Variables (.env)

```
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_16_character_app_password
```

**Where to get app password:**
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer" (or your device)
3. Google generates 16-character password
4. Copy to .env file

**Why needed?**
- Credentials never hardcoded in source code
- Can change without modifying code
- Safe to commit code to GitHub
- Different credentials per environment (local/production)

---

## API Endpoints Reference

### GET /api/gardeners
**Fetch all gardeners**
```
Response: [{id, date, name, task, email, mobile}, ...]
```

### POST /api/gardeners
**Add new gardener**
```
Body: {date, name, task, email, mobile}
Response: {id, message: "Gardener added successfully"}
```

### GET /api/gardeners/{id}
**Fetch specific gardener**
```
Response: {id, date, name, task, email, mobile}
```

### PUT /api/gardeners/{id}
**Update gardener**
```
Body: {date, name, task, email, mobile}
Response: {message: "Gardener updated successfully"}
```

### DELETE /api/gardeners/{id}
**Delete gardener**
```
Response: {message: "Gardener deleted successfully"}
```

---

## Deployment & Live Status

### ✅ LIVE ON RENDER

**Current Production Setup:**
- **URL**: https://rrbc-garden-reminder.onrender.com
- **Platform**: Render.com (Free Tier)
- **Python Version**: 3.14
- **Status**: Active and running

**Build Configuration:**
```
Build Command: pip install -r requirements.txt
Start Command: sh -c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"
```

**GitHub Repository:**
https://github.com/Chandys23/rrbc-garden-reminder (Public)

**See DEPLOYMENT_GUIDE.md for:**
- Complete setup walkthrough
- Issues encountered & solutions
- Troubleshooting guide
- Performance & scaling information

---

## Security Considerations

### What's Protected?
✅ `.env` file in `.gitignore` - Not committed to Git
✅ CORS middleware only allows browser requests
✅ Date validation prevents SQL injection
✅ Email validation checks format

### What's Not Protected? (Phase 2)
❌ No user authentication
❌ No admin login required
❌ Anyone at localhost can access
❌ No HTTPS (self-signed cert needed)

### Phase 2 Improvements
- Add admin login/password
- Use environment-specific configurations
- Deploy on HTTPS
- Add rate limiting
- Use SMS service for backup reminders

---

## Performance Considerations

### Current Setup
- **Database Queries:** Every hour for ~1000 schedules = <1 second
- **Email Sending:** ~2-5 seconds per email
- **Memory Usage:** ~50-100MB for running app
- **Concurrency:** Handles one request at a time (fine for Phase 1)

### Scaling for Phase 2
- Add database indexing (on date field)
- Use queue system (Celery) for emails
- Implement caching
- Multi-worker deployment

---

## Common Workflows

### Workflow 1: Adding Weekly Saturday Tasks

```
Monday: User adds 4 gardeners for Saturday
    Schedule 1: John - Front
    Schedule 2: Maria - Back
    Schedule 3: Ahmed - Trimming
    Schedule 4: Lisa - Front

Friday 5 PM:
    Scheduler checks: "Any Saturday schedules?"
    Finds 4 records
    Sends 4 emails to each gardener
    
Saturday 9 AM:
    Scheduler checks: "Any Saturday schedules for today?"
    Finds 4 records again
    Sends 4 reminder emails
    
Gardeners receive 2 emails throughout the weekend
```

### Workflow 2: Editing a Schedule

```
User opens http://127.0.0.1:8000
Clicks "Edit" on John's schedule
Form shows: Front task on 2026-04-19
User changes:
    - Date to 2026-04-26
    - Task to "Back"
Clicks "Save Changes"
Database updates: John's next task is Back on 2026-04-26
Next Saturday (4/25): No email to John
Following Friday (4/25): Email to John for Back task
```

### Workflow 3: Testing Emails

```
User wants to see email format before Saturday

Runs: python test_email.py

Script:
1. Loads Gmail credentials from .env
2. Creates test email with sample data
3. Connects to Gmail SMTP
4. Sends test email to user's inbox
5. Displays preview in terminal

User checks inbox
Sees exactly how reminder looks
Can adjust message if needed
```

---

## Troubleshooting Guide

### Issue: "Email not sending"

**Check:**
1. Is app running? (Terminal shows "Uvicorn running...")
2. Is .env file created? (In project root)
3. Is Gmail email correct? (Check .env)
4. Is App Password correct? (16 characters, no spaces)
5. Is 2FA enabled on Gmail account?

**Solution:**
- Restart app
- Regenerate App Password
- Check Gmail account settings

---

### Issue: "Port 8000 already in use"

**Cause:** App already running in another terminal

**Solution:**
```powershell
netstat -ano | findstr :8000
taskkill /PID [number] /F
```

---

### Issue: "ModuleNotFoundError for fastapi"

**Cause:** Virtual environment not activated or packages not installed

**Solution:**
```powershell
pip install -r requirements.txt
```

---

## Next Steps (Phase 2)

### Database
- Migrate from SQLite to PostgreSQL
- Add indexes for faster queries
- Add scheduled_by field (admin)

### Authentication
- Add login system
- Role-based access (admin/viewer)
- API key authentication

### Features
- SMS reminders via Twilio
- Recurring schedules (every week)
- Reminder history/logs
- Email templates customization
- Gardener profiles with photos

### Deployment
- Docker containerization
- Cloud hosting (Heroku, AWS)
- CI/CD pipeline
- Monitoring and logging

---

## Summary

This app demonstrates a complete full-stack system:

**Frontend:**
- User-friendly interface
- Real-time table updates
- Form validation

**Backend:**
- API design (RESTful)
- Database operations (CRUD)
- Background jobs (scheduling)
- External integrations (email)

**Database:**
- Persistent storage
- Query optimization
- Data validation

**Automation:**
- Scheduled tasks
- Email delivery
- Error handling

Great work building this! 🎉🌿

