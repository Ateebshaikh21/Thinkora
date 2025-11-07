# ⚡ Quick Deploy Guide - Thinkora

## 🎯 Fastest Way to Deploy (15 minutes)

### Step 1: Prepare Your Code (2 minutes)

1. **Push to GitHub:**

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Save logo files:**
   - `frontend/public/thinkora-logo.png`
   - `frontend/public/favicon.png`

### Step 2: Deploy Backend to Render (5 minutes)

1. Go to **https://render.com** → Sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `thinkora-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Click **"Create Web Service"**
6. **Copy the URL** (e.g., `https://thinkora-backend.onrender.com`)

### Step 3: Deploy Frontend to Vercel (5 minutes)

1. Go to **https://vercel.com** → Sign up (free)
2. Click **"New Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add Environment Variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://thinkora-backend.onrender.com/api` (your Render URL + /api)
6. Click **"Deploy"**

### Step 4: Update Backend CORS (3 minutes)

1. Go back to Render dashboard
2. Click on your backend service
3. Go to **"Environment"** tab
4. Add environment variable:
   - **Key:** `CORS_ORIGINS`
   - **Value:** `https://your-vercel-app.vercel.app` (your Vercel URL)
5. Save and redeploy

### Step 5: Test! ✅

Visit your Vercel URL and test:

- ✅ Upload documents
- ✅ Generate questions
- ✅ Take quiz
- ✅ View history

---

## 🎉 You're Live!

**Your app is now deployed and accessible worldwide!**

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://your-backend.onrender.com`
- **Cost:** $0 (Free tier)

---

## 🔧 Common Issues & Fixes

### Issue: CORS Error

**Fix:** Add your Vercel URL to `CORS_ORIGINS` in Render

### Issue: API Not Found

**Fix:** Check `VITE_API_URL` in Vercel environment variables

### Issue: Backend Sleeping (Render Free Tier)

**Fix:** First request may take 30 seconds (free tier limitation)

### Issue: Logo Not Showing

**Fix:** Make sure logo files are in `frontend/public/` before deploying

---

## 📊 What You Get (Free Tier)

**Vercel:**

- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Automatic deployments on git push

**Render:**

- ✅ 750 hours/month free
- ✅ Automatic HTTPS
- ✅ Auto-deploy on git push
- ⚠️ Sleeps after 15 min inactivity (wakes on request)

---

## 🚀 Next Steps

1. **Custom Domain:** Add your own domain in Vercel/Render settings
2. **Analytics:** Add Google Analytics
3. **Monitoring:** Set up UptimeRobot for uptime monitoring
4. **Backups:** Set up automated backups for user data

---

## 💡 Pro Tips

- **Keep Free Tier Active:** Visit your app once a day to prevent backend sleep
- **Upgrade When Ready:** $7/month on Render removes sleep limitation
- **Use MongoDB Atlas:** Free 512MB database for persistent storage
- **Enable Caching:** Improves performance and reduces API calls

---

## 📚 Need More Help?

- **Detailed Guide:** See `DEPLOYMENT_GUIDE.md`
- **Vercel Docs:** https://vercel.com/docs
- **Render Docs:** https://render.com/docs

---

**Congratulations! Your AI-powered study assistant is now live! 🎓✨**
