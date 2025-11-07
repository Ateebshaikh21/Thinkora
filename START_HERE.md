# 🚀 START HERE - Deploy Thinkora in 15 Minutes

## ✅ What's Already Done

- ✓ Git configured
- ✓ Code committed (79 files)
- ✓ Deployment configs ready
- ✓ Everything tested locally

**You're 3 steps away from going live!**

---

## 🎯 Quick Deploy Path

### STEP 1: Push to GitHub (5 min)

1. **Create repo:** https://github.com/new

   - Name: `thinkora`
   - Public repository
   - Don't add README/gitignore/license

2. **Run in Kiro terminal** (replace YOUR_USERNAME):

```powershell
& "C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/YOUR_USERNAME/thinkora.git
& "C:\Program Files\Git\cmd\git.exe" branch -M main
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```

3. **Need token?** https://github.com/settings/tokens
   - Generate new token (classic)
   - Check "repo" scope
   - Use as password when pushing

---

### STEP 2: Deploy Backend (5 min)

1. **Go to:** https://render.com
2. **Sign in** with GitHub
3. **New +** → **Web Service**
4. **Connect** your `thinkora` repo
5. **Configure:**
   ```
   Name: thinkora-backend
   Region: Oregon
   Branch: main
   Runtime: Python 3
   Build: cd backend && pip install -r requirements.txt
   Start: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
6. **Environment Variables:**
   - `PYTHON_VERSION` = `3.11.0`
   - `ENVIRONMENT` = `production`
7. **Create Web Service** → Wait 3-5 min
8. **SAVE YOUR URL:** `https://thinkora-backend-xxxx.onrender.com`

---

### STEP 3: Deploy Frontend (5 min)

1. **Go to:** https://vercel.com
2. **Sign in** with GitHub
3. **Add New** → **Project**
4. **Import** `thinkora` repo
5. **Configure:**
   ```
   Framework: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```
6. **Environment Variable:**
   - Name: `VITE_API_URL`
   - Value: `https://your-render-url.onrender.com/api`
     (Use YOUR Render URL from Step 2)
7. **Deploy** → Wait 2-3 min
8. **SAVE YOUR URL:** `https://thinkora-xxxx.vercel.app`

---

### STEP 4: Connect Them (2 min)

1. **Go to Render dashboard**
2. **Click** your backend service
3. **Environment** tab
4. **Add variable:**
   - Name: `CORS_ORIGINS`
   - Value: `https://your-vercel-url.vercel.app`
5. **Save** → Wait for redeploy

---

## 🎉 Test Your Live App!

Open your Vercel URL and try:

- Upload a document
- Generate questions
- Take a quiz
- View history

---

## 📚 Detailed Guides

- **Git help:** `PUSH_TO_GITHUB.md`
- **Full deployment:** `NEXT_STEPS.md`
- **Track progress:** `DEPLOYMENT_PROGRESS.md`

---

## 🆘 Quick Fixes

**Git error "remote exists":**

```powershell
& "C:\Program Files\Git\cmd\git.exe" remote remove origin
```

**Render build fails:**

- Check Python version is 3.11.0
- Verify build command has `cd backend`

**Vercel build fails:**

- Check root directory is `frontend`
- Verify VITE_API_URL ends with `/api`

**CORS errors:**

- Add Vercel URL to Render CORS_ORIGINS
- Make sure no trailing slash

---

## ✅ You're Ready!

**Total time:** 15 minutes
**Current step:** Push to GitHub

**Let's go! 🚀**
