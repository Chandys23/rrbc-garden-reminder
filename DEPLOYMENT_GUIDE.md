# Deployment Guide - Render.com (Updated & Verified Working)

🎉 **Status: APP IS LIVE!** This guide documents the successful deployment and troubleshooting steps.

## ✅ Deployment Verification

Your live app is deployed at Render with the following settings:

**Service Details:**
- **App Name**: rrbc-garden-reminder
- **Live URL**: https://rrbc-garden-reminder.onrender.com
- **Environment**: Python 3.14
- **Instance Type**: Free tier
- **GitHub Repo**: https://github.com/Chandys23/rrbc-garden-reminder

---

## Pre-Deployment Requirements

### 1. GitHub Repository ✅
Make sure your repo is:
- **Public** (not private - Render needs access)
- **Contains all files**: backend/, frontend/, requirements.txt, .gitignore, etc.
- **Committed and pushed** to main branch

### 2. Environment Variables ✅
Set these on Render Dashboard (Settings → Environment):
- `GMAIL_EMAIL` = your_email@gmail.com
- `GMAIL_PASSWORD` = your_16_character_app_password

Get app password: https://myaccount.google.com/apppasswords

---

## Verified Working Configuration

### Build Command ✅
```
pip install -r requirements.txt
```

### Start Command ✅ (IMPORTANT!)
```
sh -c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"
```

⚠️ **Must use `sh -c "cd backend && ..."` format** - earlier versions failed without changing directory first!

### Root Directory
**Leave this BLANK** (empty) - do NOT set to "backend"

### requirements.txt Versions (Render-Compatible)
```
fastapi==0.95.0
uvicorn==0.21.0
python-dotenv==1.0.0
apscheduler==3.11.2
requests==2.31.0
setuptools==65.5.0
```

⚠️ **Important Notes:**
- Older versions avoid Rust compilation (pydantic-core issues)
- Removed sqlalchemy (using sqlite3 directly)
- Removed email-validator (not needed)
- Added setuptools (required for pkg_resources)
- apscheduler 3.11.2 is compatible with Python 3.14

---

## Deployment Steps (Complete)

### Step 1: Make Repository Public
1. Go to https://github.com/Chandys23/rrbc-garden-reminder
2. Settings → Change repository visibility to **Public**

### Step 2: Verify Files on GitHub
All these should be visible on your GitHub repo page:
- ✅ backend/main.py
- ✅ backend/database.py
- ✅ backend/reminders.py
- ✅ frontend/index.html
- ✅ requirements.txt
- ✅ README.md
- ✅ .gitignore
- ✅ DEPLOYMENT_GUIDE.md

### Step 3: Create Render Service
1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Select **rrbc-garden-reminder** from repo list
   - If not showing: GitHub permissions need renewal
4. Fill in settings (see **Verified Working Configuration** section)
5. Click **"Create Web Service"**

### Step 4: Add Environment Variables
1. On Render dashboard, go to Settings
2. Find **Environment** section
3. Add 2 variables:
   - `GMAIL_EMAIL` = chandan.s23@gmail.com (your Gmail)
   - `GMAIL_PASSWORD` = vzbt_fmhy_udpt_uhpa (your 16-char app password)
4. Click Save

### Step 5: Deploy & Monitor
1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Click **"Logs"** tab to watch build progress
3. Watch for success message or errors
4. Once live, your app URL will be shown

---

## Issues Encountered & Resolutions

### ❌ Issue #1: Repository Visibility
**Error**: Render can't see the repository

**Cause**: Repository was set to Private

**Resolution**: Changed to Public on GitHub Settings

---

### ❌ Issue #2: Missing Files on GitHub
**Error**: `requirements.txt` not found during build

**Cause**: Files weren't properly pushed; initial commit only had README and .gitignore

**Resolution**: 
```bash
git add -A
git commit -m "Add all project files"
git push -f origin main
```

---

### ❌ Issue #3: Root Directory Conflict
**Error**: `Root directory 'backend' does not exist`

**Cause**: Set Root Directory to "backend", which broke the relative path to requirements.txt

**Resolution**: 
1. Left Root Directory **blank**
2. Changed Start Command to: `sh -c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"`

---

### ❌ Issue #4: Pydantic-Core Compilation Error
**Error**: 
```
× Preparing metadata (pyproject.toml) did not run successfully
Caused by: maturin failed
error: failed to create directory `/usr/local/.../cargo/registry`
Caused by: Read-only file system (os error 30)
```

**Cause**: Render's free tier has read-only filesystem; newer pydantic versions need Rust compilation from source

**Resolution**: Downgraded to `fastapi==0.95.0` and `pydantic` via dependencies (not explicit) - these versions have pre-built wheels

---

### ❌ Issue #5: Missing pkg_resources Module
**Error**: 
```
ModuleNotFoundError: No module named 'pkg_resources'
```

**Cause**: `setuptools` not in requirements.txt

**Resolution**: Added `setuptools==65.5.0` to requirements.txt

---

### ❌ Issue #6: pkgutil.ImpImporter Deprecation
**Error**: 
```
AttributeError: module 'pkgutil' has no attribute 'ImpImporter'
```

**Cause**: `apscheduler==3.10.1` is incompatible with Python 3.14

**Resolution**: Upgraded to `apscheduler==3.11.2` (latest stable)

---

### ❌ Issue #7: Database Module Not Found
**Error**: 
```
ModuleNotFoundError: No module named 'database'
```

**Cause**: Start Command was `python -m uvicorn backend.main:app` which imports `database` from root instead of from `backend/`

**Resolution**: Changed to:
```
sh -c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"
```

This changes working directory to backend/ first, making relative imports work

---

## Post-Deployment Setup

### 1. Verify App is Live
1. Go to your app URL
2. You should see the Garden Care Reminder interface
3. Test adding a new gardener schedule
4. Verify table updates correctly

### 2. Test Email Functionality
1. Add a gardener with:
   - **Name**: Test Gardener
   - **Date**: Tomorrow's date
   - **Task**: Front
   - **Email**: your_email@gmail.com
2. Check your email for reminder (may take ~1 hour for scheduler to run)
3. Go to Render → Logs to verify scheduler is working

### 3. Monitor Logs
Watch for these messages (Logs tab):
```
✓ Database initialized
✓ Reminder scheduler started
📧 Sending reminder to [name]
✓ Email sent to [email]
```

---

## Important Limitations & Notes

### 📌 Database Persistence
⚠️ **SQLite on Render (Free Tier)**: File-based database `gardeners.db` is stored on ephemeral filesystem.

**What happens**:
- Data persists while app is running
- Data is **LOST** when:
  - Render service restarts
  - You redeploy
  - Free tier service goes to sleep (after 15 min inactivity + restart)

**When you're ready to scale**:
1. Migrate to Render PostgreSQL (free tier available)
2. Update `backend/database.py` to use PostgreSQL instead of SQLite
3. Add `psycopg2-binary==2.9.0` to requirements.txt

---

### 📌 Cold Starts
Free tier services sleep after 15 minutes of inactivity.

**Expected behavior**:
- First request after sleep: 10-30 seconds (waking up)
- Subsequent requests: Normal speed

**Solution**: Upgrade to paid tier if you need always-on availability

---

### 📌 Email Reminders
The background scheduler runs every hour to check for reminders.

**How it works**:
1. APScheduler starts on app startup
2. Every 1 hour: checks all gardener schedules
3. If scheduled_date matches today or yesterday → send reminder
4. If app crashes/restarts → scheduler restarts and continues

**Note**: Reminders won't send if app is sleeping (free tier inactivity)

---

## Updating Your App

### Make Local Changes
```bash
# Edit files locally
# Test locally first
```

### Push to GitHub
```bash
git add .
git commit -m "Description of changes"
git push
```

### Deploy on Render
**Option A (Auto-Deploy)**: Enable in Settings → Auto-Deploy
- Every push automatically triggers rebuild/deploy

**Option B (Manual Deploy)**:
1. Go to Render Dashboard
2. Select your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| **App won't start** | Missing dependencies | Check logs; update requirements.txt |
| **ModuleNotFoundError: database** | Wrong Start Command | Use: `sh -c "cd backend && python -m uvicorn main:app..."` |
| **Emails not sending** | Wrong Gmail password | Regenerate at myaccount.google.com/apppasswords |
| **GMAIL_EMAIL env var not set** | Typo in key name | Must be exactly `GMAIL_EMAIL` (case-sensitive) |
| **Read-only filesystem error** | Old pydantic version | Downgrade fastapi to 0.95.0 |
| **pkgutil warning** | Missing setuptools | Add `setuptools==65.5.0` to requirements.txt |
| **Site not reachable** | Service crashed | Check logs; fix error and redeploy |

---

## Performance & Scaling

**Current Free Tier Specs**:
- CPU: Shared
- RAM: 512 MB
- Uptime: 750 hours/month (auto-stops after 15 min inactivity)
- Database: Ephemeral (data lost on restart)

**For Production Use**:
1. Upgrade to paid instance ($7+/month)
2. Add PostgreSQL database ($15+/month)
3. Enable auto-deploy for continuous updates
4. Set up monitoring/alerts

---

## Success Checklist

- ✅ Repository is public on GitHub
- ✅ All files pushed to main branch
- ✅ Render service created and named
- ✅ Build Command: `pip install -r requirements.txt`
- ✅ Start Command: `sh -c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"`
- ✅ Root Directory: **BLANK**
- ✅ Environment variables set: GMAIL_EMAIL, GMAIL_PASSWORD
- ✅ requirements.txt has correct versions
- ✅ App deployed successfully
- ✅ App accessible at live URL
- ✅ Can add/edit/delete gardener schedules
- ✅ Logs show "✓ Reminder scheduler started"

---

## Next Steps

1. ✅ App is live - Start using it!
2. Test adding schedules and verify reminders work
3. Share the live URL with team members
4. When ready: Upgrade to persistent database (PostgreSQL)
5. Monitor logs for any issues

Need help? Check: https://render.com/docs/troubleshooting-deploys
