# Deployment Guide

This guide will help you deploy the AI Brochure Generator to run online.

## Option 1: Render.com (Recommended - Free Tier Available)

### Steps:

1. **Push your code to GitHub** (already done ✅)

2. **Go to Render.com**
   - Visit: https://render.com
   - Sign up/login with your GitHub account

3. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Yashashvi211189/Ai_Brochure`
   - Select the repository

4. **Configure the Service**
   - **Name**: `ai-brochure-generator` (or any name you like)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or `.` if needed)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (usually 2-5 minutes)
   - Your app will be live at: `https://ai-brochure-generator.onrender.com` (or your custom name)

### Render.com Free Tier:
- ✅ Free SSL certificate
- ✅ Custom domain support
- ⚠️ Spins down after 15 minutes of inactivity (first request may be slow)
- ✅ 750 hours/month free

---

## Option 2: Railway.app (Alternative Free Option)

### Steps:

1. **Go to Railway.app**
   - Visit: https://railway.app
   - Sign up/login with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Yashashvi211189/Ai_Brochure`

3. **Configure**
   - Railway auto-detects Python
   - It will use the `Procfile` automatically
   - No additional config needed

4. **Deploy**
   - Click "Deploy"
   - Railway will build and deploy automatically
   - Get your URL from the "Settings" → "Domains"

### Railway Free Tier:
- ✅ $5 free credit monthly
- ✅ No sleep (always on)
- ✅ Custom domain support

---

## Option 3: PythonAnywhere (Simple Python Hosting)

### Steps:

1. **Sign up at PythonAnywhere**
   - Visit: https://www.pythonanywhere.com
   - Create a free account

2. **Open a Bash Console**
   - Click "Consoles" → "Bash"

3. **Clone your repo**
   ```bash
   git clone https://github.com/Yashashvi211189/Ai_Brochure.git
   cd Ai_Brochure
   ```

4. **Install dependencies**
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

5. **Create a WSGI file**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask → Python 3.10
   - Edit the WSGI file to point to your app:
   ```python
   import sys
   path = '/home/yourusername/Ai_Brochure'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

6. **Configure Static Files**
   - In "Web" tab → "Static files"
   - Add mapping: `/static/` → `/home/yourusername/Ai_Brochure/static/`

7. **Reload Web App**
   - Click "Reload" button
   - Your app will be at: `https://yourusername.pythonanywhere.com`

---

## Environment Variables (if needed)

If you want to use real OpenAI API (instead of stubbed version), add:
- `OPENAI_API_KEY`: Your OpenAI API key

In Render/Railway: Add in "Environment" section
In PythonAnywhere: Add in "Web" → "Environment variables"

---

## Quick Deploy Commands (Render)

After connecting GitHub repo, Render will auto-detect:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

That's it! The `render.yaml` file handles the rest.

---

## Troubleshooting

### If deployment fails:
1. Check build logs for errors
2. Ensure all dependencies are in `requirements.txt`
3. Verify Python version compatibility (3.9+)
4. Check that `gunicorn` is in requirements.txt

### If app doesn't start:
1. Check start command is correct: `gunicorn app:app`
2. Verify port binding (Render/Railway handle this automatically)
3. Check logs for runtime errors

---

## Recommended: Render.com

**Why Render?**
- ✅ Easiest setup
- ✅ Free tier available
- ✅ Auto-deploys on git push
- ✅ Free SSL
- ✅ Good documentation

**Your deployment URL will be:**
```
https://ai-brochure-generator.onrender.com
```
(Or whatever name you choose)
