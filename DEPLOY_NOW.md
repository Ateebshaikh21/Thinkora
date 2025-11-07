# 🚀 Deploy Thinkora NOW - Step by Step

## ⚡ Follow These Exact Steps

### 📋 Prerequisites

- [ ] GitHub account (create at https://github.com if you don't have one)
- [ ] Vercel account (sign up at https://vercel.com with GitHub)
- [ ] Render account (sign up at https://render.com with GitHub)

---

## STEP 1: Push Code to GitHub (5 minutes)

### 1.1 Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit - Thinkora AI Study Assistant"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `thinkora`
3. Description: `AI-Powered Smart Study Assistant`
4. Keep it **Public** (or Private if you prefer)
5. **DO NOT** initialize with README (we already have one)
6. Click **"Create repository"**

### 1.3 Push to GitHub

Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/thinkora.git
git branch -M main
git push -u origin main
```

✅ **Checkpoint:** Your code should now be visible on GitHub!

---

## STEP 2: Deploy Backend to Render (7 minutes)

### 2.1 Go to Render

1. Open https://render.com
2. Click **"Get Started"** or **"Sign In"**
3. Sign in with GitHub

### 2.2 Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect a repository"**
4. Find and select your **`thinkora`** repository
5. Click **"Connect"**

### 2.3 Configure Service

Fill in these EXACT values:

**Basic Settings:**

- **Name:** `thinkora-backend`
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch:** `main`
- **Root Directory:** Leave empty
- **Runtime:** `Python 3`

**Build & Deploy:**

- **Build Command:**
  ```
  cd backend && pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**

- Select **"Free"** (0.1 CPU, 512 MB RAM)

### 2.4 Add Environment Variables (Optional but recommended)

Click **"Advanced"** → **"Add Environment Variable"**

Add these:

- **Key:** `ENVIRONMENT` | **Value:** `production`
- **Key:** `PYTHON_VERSION` | **Value:** `3.11.0`

### 2.5 Deploy!

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. **COPY YOUR BACKEND URL** (e.g., `https://thinkora-backend.onrender.com`)

✅ **Checkpoint:** You should see "Your service is live 🎉"

---

## STEP 3: Deploy Frontend to Vercel (5 minutes)

### 3.1 Go to Vercel

1. Open https://vercel.com
2. Click **"Sign Up"** or **"Login"**
3. Sign in with GitHub

### 3.2 Import Project

1. Click **"Add New..."** → **"Project"**
2. Find your **`thinkora`** repository
3. Click **"Import"**

### 3.3 Configure Project

Fill in these EXACT values:

**Project Settings:**

- **Framework Preset:** `Vite`
- **Root Directory:** `frontend` (click Edit and type `frontend`)
- **Build Command:** `npm run build` (should auto-detect)
- **Output Directory:** `dist` (should auto-detect)
- **Install Command:** `npm install` (should auto-detect)

### 3.4 Add Environment Variable

Click **"Environment Variables"** section:

- **Key:** `VITE_API_URL`
- **Value:** `https://thinkora-backend.onrender.com/api`
  (⚠️ Use YOUR Render URL from Step 2.5 + `/api`)

### 3.5 Deploy!

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. **COPY YOUR FRONTEND URL** (e.g., `https://thinkora-xyz.vercel.app`)

✅ **Checkpoint:** You should see "Congratulations! 🎉"

---

## STEP 4: Update Backend CORS (3 minutes)

### 4.1 Go Back to Render

1. Open https://dashboard.render.com
2. Click on your **`thinkora-backend`** service

### 4.2 Add CORS Environment Variable

1. Click **"Environment"** tab (left sidebar)
2. Click **"Add Environment Variable"**
3. Add:
   - **Key:** `CORS_ORIGINS`
   - **Value:** `https://thinkora-xyz.vercel.app`
     (⚠️ Use YOUR Vercel URL from Step 3.5)

### 4.3 Save and Redeploy

1. Click **"Save Changes"**
2. Service will automatically redeploy (wait 2-3 minutes)

✅ **Checkpoint:** Backend should restart with new CORS settings

---

## STEP 5: Test Your Deployment! (2 minutes)

### 5.1 Open Your App

Go to your Vercel URL: `https://thinkora-xyz.vercel.app`

### 5.2 Test Features

- [ ] Home page loads ✅
- [ ] Click "Start Studying Smart"
- [ ] Create a subject
- [ ] Upload a document (try a PDF)
- [ ] Generate questions
- [ ] Take a quiz
- [ ] Check history

### 5.3 Troubleshooting

**If you see CORS errors:**

- Check that CORS_ORIGINS in Render matches your Vercel URL exactly
- Make sure there's no trailing slash

**If API calls fail:**

- Check VITE_API_URL in Vercel environment variables
- Make sure it ends with `/api`
- Verify backend is running on Render

**If backend is slow (first request):**

- This is normal on Render free tier (cold start ~30 seconds)
- Subsequent requests will be fast

---

## 🎉 SUCCESS! You're Live!

Your app is now deployed and accessible worldwide!

**Your URLs:**

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://your-backend.onrender.com`

**Share with friends and start helping students! 🎓✨**

---

## 📊 What You Get (Free Tier)

**Vercel:**

- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Auto-deploy on git push
- ✅ 100 GB bandwidth/month

**Render:**

- ✅ 750 hours/month free
- ✅ Automatic HTTPS
- ✅ Auto-deploy on git push
- ⚠️ Sleeps after 15 min inactivity (wakes on first request)

---

## 🔄 Future Updates

To update your app:

```bash
git add .
git commit -m "Your update message"
git push
```

Both Vercel and Render will automatically deploy your changes!

---

## 🆘 Need Help?

**Common Issues:**

1. **"Repository not found"**

   - Make sure repository is public or grant Vercel/Render access

2. **"Build failed"**

   - Check build logs in Vercel/Render dashboard
   - Verify all dependencies are in requirements.txt and package.json

3. **"Cannot connect to backend"**

   - Verify VITE_API_URL is correct
   - Check backend is running on Render

4. **"CORS error"**
   - Update CORS_ORIGINS in Render with exact Vercel URL

---

## 💡 Pro Tips

1. **Custom Domain:** Add your own domain in Vercel settings (free)
2. **Keep Backend Awake:** Use UptimeRobot to ping every 5 minutes
3. **Monitor:** Set up Sentry for error tracking
4. **Upgrade:** $7/month on Render removes sleep limitation

---

## 📝 Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] CORS configured
- [ ] App tested and working
- [ ] URLs saved for future reference

---

**Congratulations! You've successfully deployed Thinkora! 🚀🎓**

Now go help students ace their exams with AI-powered study assistance!
