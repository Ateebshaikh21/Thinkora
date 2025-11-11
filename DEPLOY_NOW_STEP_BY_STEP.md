# 🚀 Deploy Thinkora to Production - Step by Step

## ✅ Current Status

- Quiz bug fixed ✓
- Google Authentication added ✓
- All changes committed ✓
- Ready to deploy!

---

## 📋 Deployment Plan

**Deploy Order:**

1. Push to GitHub (2 min)
2. Deploy Backend to Render (5 min)
3. Deploy Frontend to Vercel (3 min)
4. Connect CORS (1 min)
5. Add Firebase later (optional)

**Total Time: ~15 minutes**

---

## STEP 1: Push to GitHub (2 minutes)

### Option A: GitHub Desktop (Easiest)

1. Download: https://desktop.github.com
2. Open GitHub Desktop
3. Sign in with your account
4. File → Add Local Repository
5. Select: `C:\Users\Admin\OneDrive\Documents\Projects\Thinkora`
6. Click "Publish repository" or "Push origin"
7. ✅ Done!

### Option B: Command Line

```powershell
cd "C:\Users\Admin\OneDrive\Documents\Projects\Thinkora"
git push -u origin main
```

Enter your GitHub credentials when prompted.

### Option C: Run the Script

```powershell
.\push-to-github.ps1
```

---

## STEP 2: Deploy Backend to Render (5 minutes)

### If First Time Deploying:

1. **Go to:** https://render.com
2. **Sign in** with GitHub
3. **Click:** "New +" → "Web Service"
4. **Connect** your `Thinkora` repository
5. **Configure:**

   ```
   Name: thinkora-backend
   Region: Oregon (US West)
   Branch: main
   Runtime: Python 3

   Build Command:
   cd backend && pip install -r requirements.txt

   Start Command:
   cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT

   Instance Type: Free
   ```

6. **Add Environment Variables:**

   - `PYTHON_VERSION` = `3.11.0`
   - `ENVIRONMENT` = `production`

7. **Click:** "Create Web Service"
8. **Wait:** 3-5 minutes for build
9. **Save URL:** `https://thinkora-backend-xxxx.onrender.com`

### If Already Deployed:

1. Go to: https://dashboard.render.com
2. Click your "thinkora-backend" service
3. Click "Manual Deploy" → "Deploy latest commit"
4. Wait 3-5 minutes
5. ✅ Updated!

---

## STEP 3: Deploy Frontend to Vercel (3 minutes)

### If First Time Deploying:

1. **Go to:** https://vercel.com
2. **Sign in** with GitHub
3. **Click:** "Add New..." → "Project"
4. **Import** your `Thinkora` repository
5. **Configure:**

   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

6. **Add Environment Variable:**

   - Name: `VITE_API_URL`
   - Value: `https://YOUR-RENDER-URL.onrender.com/api`
     (Use your Render URL from Step 2)

7. **Click:** "Deploy"
8. **Wait:** 2-3 minutes
9. **Save URL:** `https://thinkora-xxxx.vercel.app`

### If Already Deployed:

1. Vercel auto-deploys when you push to GitHub! 🎉
2. Go to: https://vercel.com/dashboard
3. Check deployment status
4. Wait 2-3 minutes
5. ✅ Updated!

---

## STEP 4: Connect Frontend & Backend (1 minute)

1. **Go to:** https://dashboard.render.com
2. **Click** your "thinkora-backend" service
3. **Click** "Environment" tab
4. **Add/Update variable:**
   - Key: `CORS_ORIGINS`
   - Value: `https://your-vercel-url.vercel.app`
     (Use YOUR Vercel URL from Step 3, NO trailing slash!)
5. **Click:** "Save Changes"
6. **Wait:** 1-2 minutes for redeploy

---

## STEP 5: Test Your Live App! 🎉

1. **Open** your Vercel URL
2. **Test features:**
   - Home page loads ✓
   - Upload document ✓
   - Generate questions ✓
   - Take quiz (with fixed answer selection!) ✓
   - View results ✓
   - Check history ✓

---

## STEP 6: Add Firebase (Later - Optional)

**For now, the app works without authentication.**
It uses "demo_user" for all data.

**When ready to add Google Sign-In:**

1. Follow `FIREBASE_SETUP_GUIDE.md`
2. Add Firebase config to Vercel environment variables
3. Redeploy
4. Students can sign in with Google!

---

## 🎯 What's Deployed

### Features Live:

✅ Document upload & processing
✅ AI question generation
✅ Interactive quizzes (with fixed answer bug!)
✅ Performance analytics
✅ Learning history
✅ CSV export
✅ Responsive design

### Coming Soon (After Firebase Setup):

🔜 Google Sign-In
🔜 Personal student accounts
🔜 Private data per student
🔜 Multi-user support

---

## 📝 Your URLs

**GitHub:** https://github.com/chauhansneha674-ops/Thinkora

**Backend (Render):** ************\_************

**Frontend (Vercel):** ************\_************

---

## 🆘 Troubleshooting

### Push to GitHub fails:

- Use GitHub Desktop (easiest)
- Or get Personal Access Token: https://github.com/settings/tokens

### Render build fails:

- Check Python version is 3.11.0
- Verify build command has `cd backend`
- Check logs for errors

### Vercel build fails:

- Check root directory is `frontend`
- Verify VITE_API_URL is set correctly
- Check build logs

### CORS errors:

- Add Vercel URL to Render CORS_ORIGINS
- No trailing slash in URL
- Wait for Render to redeploy

### Firebase not working:

- That's OK! Deploy without it first
- Add Firebase config later
- App works with demo_user for now

---

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] CORS configured
- [ ] App tested and working
- [ ] URLs saved

---

## 📚 Next Steps After Deployment

1. **Share your app!**

   - Send Vercel URL to friends/testers
   - Get feedback
   - Iterate

2. **Add Firebase** (when ready)

   - Follow FIREBASE_SETUP_GUIDE.md
   - Add config to Vercel
   - Enable Google Sign-In

3. **Monitor usage**

   - Check Render dashboard
   - Check Vercel analytics
   - Review logs

4. **Optional enhancements**
   - Custom domain
   - MongoDB for persistence
   - OpenAI API for AI features

---

**Ready to deploy? Start with Step 1!** 🚀
