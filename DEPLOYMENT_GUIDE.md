# Deployment Guide - Render.com

This guide explains how to deploy the RRBC Garden Care Reminder App to Render (free tier).

## Why Render?

- **Free tier** includes hosting for web services
- **Easy deployment** from GitHub
- **Auto-restarts** on failure
- **Environment variables** support for sensitive data
- **Simple scaling** when needed

## Pre-Deployment Steps

### 1. Push to GitHub

1. Initialize git (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create a GitHub repository and push:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/rrbc-garden-reminder.git
   git branch -M main
   git push -u origin main
   ```

### 2. Environment Variables

Before deploying, ensure you have:
- `GMAIL_EMAIL` - Your Gmail address for sending reminders
- `GMAIL_PASSWORD` - Your Gmail app password (generated at https://myaccount.google.com/apppasswords)

## Deployment Steps

### 1. Create a Render Account
- Go to https://render.com
- Sign up with GitHub

### 2. Create a New Web Service
1. Click **"New +"** → **"Web Service"**
2. Select your GitHub repository
3. Fill in the settings:
   - **Name**: `rrbc-garden-reminder` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

### 3. Add Environment Variables
1. Scroll to **Environment** section
2. Add these variables:
   ```
   GMAIL_EMAIL=your_email@gmail.com
   GMAIL_PASSWORD=your_16_char_app_password
   ```

### 4. Deploy
- Click **"Create Web Service"**
- Render will automatically build and deploy your app
- Wait for the deployment to complete (2-5 minutes)
- Your app URL: `https://rrbc-garden-reminder.onrender.com` (example)

## Important Limitations & Solutions

### **Database Note**
⚠️ **SQLite on Render:** Render's filesystem is ephemeral (temporary). Any data saved to `gardeners.db` will be lost when the service restarts or redeploys.

**Solution:** Consider upgrading to PostgreSQL when needed. Render offers free PostgreSQL databases:
1. Create a PostgreSQL database on Render
2. Update `database.py` to use PostgreSQL instead of SQLite
3. Add `psycopg2-binary` to requirements.txt

### **Cold Starts**
Free tier services sleep after 15 minutes of inactivity. First request after sleep takes 5-10 seconds. This is normal.

### **Email Reminders**
The background scheduler runs during app uptime. If the app restarts, reminders will continue after startup. For reliability, consider:
- Using CRON jobs (Render offers this)
- External email service with webhooks

## Post-Deployment Verification

1. Visit your app URL: `https://rrbc-garden-reminder.onrender.com`
2. Test adding a new gardener schedule
3. Test editing/deleting schedules
4. Verify the email function (add a test schedule and check logs)

## View Logs

- Go to your web service on Render
- Click **"Logs"** tab to view real-time logs
- Useful for debugging issues

## Updating Your App

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```
3. Render automatically rebuilds and redeploys (optional: enable auto-deploy in settings)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **App won't start** | Check logs for errors; ensure `requirements.txt` has all dependencies |
| **404 on root URL** | Verify `Procfile` start command is correct |
| **Emails not sending** | Check Gmail app password is correct; verify GMAIL_EMAIL env var |
| **Service keeps restarting** | Check memory usage; free tier has 512MB limit |

## Next Steps

1. ✅ Push to GitHub
2. ✅ Deploy to Render
3. Optional: Set up PostgreSQL for persistent data
4. Optional: Configure CRON jobs for reliable email scheduling

---

Need help? Check Render docs: https://render.com/docs
