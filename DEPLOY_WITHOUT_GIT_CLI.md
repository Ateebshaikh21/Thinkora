# 🚀 Deploy Thinkora Without Git Command Line

## Use GitHub Desktop Instead!

If you don't want to use Git command line, you can use GitHub Desktop (GUI application).

---

## STEP 1: Install GitHub Desktop (3 minutes)

1. **Download:**

   - Go to: https://desktop.github.com
   - Click "Download for Windows"
   - Run the installer

2. **Sign In:**
   - Open GitHub Desktop
   - Click "Sign in to GitHub.com"
   - Enter your GitHub credentials
   - (If you don't have an account, create one at https://github.com)

---

## STEP 2: Publish Your Project (2 minutes)

1. **Add Repository:**

   - In GitHub Desktop, click "File" → "Add local repository"
   - Click "Choose..." and select your Thinkora folder
   - Click "Add repository"

2. **If it says "not a git repository":**

   - Click "create a repository"
   - Name: `thinkora`
   - Description: `AI-Powered Smart Study Assistant`
   - Keep "Initialize with README" UNCHECKED
   - Click "Create Repository"

3. **Commit Changes:**

   - You'll see all your files listed
   - In the bottom left, enter commit message: `Initial commit - Thinkora`
   - Click "Commit to main"

4. **Publish to GitHub:**
   - Click "Publish repository" button (top right)
   - Name: `thinkora`
   - Description: `AI-Powered Smart Study Assistant`
   - Keep "Keep this code private" UNCHECKED (or check if you want private)
   - Click "Publish Repository"

✅ **Done!** Your code is now on GitHub!

---

## STEP 3: Deploy Backend to Render (5 minutes)

1. **Go to Render:**

   - Open: https://render.com
   - Click "Get Started" or "Sign In"
   - Sign in with GitHub

2. **Create Web Service:**

   - Click "New +" → "Web Service"
   - You'll see your `thinkora` repository
   - Click "Connect"

3. **Configure:**

   ```
   Name: thinkora-backend
   Region: Oregon (or closest to you)
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3

   Build Command:
   cd backend && pip install -r requirements.txt

   Start Command:
   cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT

   Instance Type: Free
   ```

4. **Add Environment Variables:**

   - Click "Advanced"
   - Add: `ENVIRONMENT` = `production`
   - Add: `PYTHON_VERSION` = `3.11.0`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes
   - **COPY YOUR URL:** `https://thinkora-backend-xxxx.onrender.com`

---

## STEP 4: Deploy Frontend to Vercel (5 minutes)

1. **Go to Vercel:**

   - Open: https://vercel.com
   - Click "Sign Up" or "Login"
   - Sign in with GitHub

2. **Import Project:**

   - Click "Add New..." → "Project"
   - Find your `thinkora` repository
   - Click "Import"

3. **Configure:**

   ```
   Framework Preset: Vite
   Root Directory: frontend (click Edit and type "frontend")
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Add Environment Variable:**

   - In "Environment Variables" section:
   - Name: `VITE_API_URL`
   - Value: `https://your-render-url.onrender.com/api`
     (Use YOUR Render URL from Step 3 + `/api`)

5. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes
   - **COPY YOUR URL:** `https://thinkora-xxxx.vercel.app`

---

## STEP 5: Update CORS (3 minutes)

1. **Go to Render Dashboard:**

   - Open: https://dashboard.render.com
   - Click on your `thinkora-backend` service

2. **Add CORS:**

   - Click "Environment" tab
   - Click "Add Environment Variable"
   - Name: `CORS_ORIGINS`
   - Value: `https://your-vercel-url.vercel.app`
     (Use YOUR Vercel URL from Step 4)

3. **Save:**
   - Click "Save Changes"
   - Wait 2-3 minutes for redeploy

---

## STEP 6: Test Your App! ✅

1. Open your Vercel URL in browser
2. Test all features:
   - Upload document
   - Generate questions
   - Take quiz
   - View history

---

## 🎉 Success!

Your app is now live!

**URLs:**

- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.onrender.com`

---

## 🔄 Future Updates

To update your app:

1. Make changes in your code
2. Open GitHub Desktop
3. You'll see changed files
4. Enter commit message
5. Click "Commit to main"
6. Click "Push origin"

Both Vercel and Render will auto-deploy! 🚀

---

## 💡 Benefits of GitHub Desktop

- ✅ No command line needed
- ✅ Visual interface
- ✅ Easy to use
- ✅ See all changes clearly
- ✅ Simple commit and push

---

## 🆘 Troubleshooting

**Can't find repository in Render/Vercel?**

- Make sure you published to GitHub
- Check repository is public or grant access

**Build failed?**

- Check build logs in dashboard
- Verify all files are committed

**CORS error?**

- Update CORS_ORIGINS in Render
- Make sure URL matches exactly

---

**This method is easier if you're not comfortable with command line!** 🎯
