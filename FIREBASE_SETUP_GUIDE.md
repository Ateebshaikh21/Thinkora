# 🔥 Firebase Setup Guide for Google Authentication

## Step 1: Create Firebase Project (5 minutes)

1. **Go to Firebase Console:**

   - Visit: https://console.firebase.google.com
   - Click "Add project" or "Create a project"

2. **Project Setup:**
   - Project name: `Thinkora` (or any name you like)
   - Click "Continue"
   - Disable Google Analytics (optional, not needed for auth)
   - Click "Create project"
   - Wait for project creation
   - Click "Continue"

## Step 2: Enable Google Authentication

1. **In Firebase Console:**
   - Click "Authentication" in the left sidebar
   - Click "Get started"
   - Click "Sign-in method" tab
   - Click "Google" provider
   - Toggle "Enable"
   - Select a support email (your email)
   - Click "Save"

## Step 3: Register Web App

1. **Add Web App:**

   - Click the gear icon (⚙️) → "Project settings"
   - Scroll down to "Your apps"
   - Click the web icon (`</>`)
   - App nickname: `Thinkora Web`
   - Check "Also set up Firebase Hosting" (optional)
   - Click "Register app"

2. **Copy Firebase Config:**
   You'll see something like this:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     authDomain: "thinkora-xxxxx.firebaseapp.com",
     projectId: "thinkora-xxxxx",
     storageBucket: "thinkora-xxxxx.appspot.com",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:xxxxxxxxxxxxx",
   };
   ```
   **COPY THESE VALUES!** You'll need them next.

## Step 4: Add Config to Your Project

1. **Create `.env` file in frontend folder:**

   ```bash
   cd frontend
   ```

2. **Create file:** `frontend/.env`

   ```env
   VITE_FIREBASE_API_KEY=your_api_key_here
   VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain_here
   VITE_FIREBASE_PROJECT_ID=your_project_id_here
   VITE_FIREBASE_STORAGE_BUCKET=your_storage_bucket_here
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id_here
   VITE_FIREBASE_APP_ID=your_app_id_here
   ```

3. **Replace values** with your Firebase config from Step 3

## Step 5: Install Dependencies

```bash
cd frontend
npm install firebase
```

## Step 6: Test Locally

1. **Start backend:**

   ```bash
   cd backend
   python start.py
   ```

2. **Start frontend:**

   ```bash
   cd frontend
   npm run dev
   ```

3. **Open browser:**
   - Go to: http://localhost:3000
   - You should see the login page
   - Click "Continue with Google"
   - Select your Google account
   - You should be logged in!

## Step 7: Add Authorized Domains (For Production)

1. **In Firebase Console:**
   - Go to Authentication → Settings → Authorized domains
   - Add your production domains:
     - `your-app.vercel.app` (Vercel domain)
     - `your-custom-domain.com` (if you have one)

## 🎉 Done!

Your Google Authentication is now set up!

## 🔒 Security Notes

- ✅ `.env` file is in `.gitignore` (credentials won't be committed)
- ✅ Firebase API keys are safe to expose (they're restricted by domain)
- ✅ Use environment variables in production (Vercel/Render)

## 📝 Environment Variables for Production

**Vercel (Frontend):**

- Add all `VITE_FIREBASE_*` variables in Vercel dashboard

**Render (Backend):**

- Add `FIREBASE_PROJECT_ID` for token verification

## 🆘 Troubleshooting

**"Firebase: Error (auth/unauthorized-domain)"**

- Add your domain to Authorized domains in Firebase Console

**"Firebase: Error (auth/popup-blocked)"**

- Allow popups in browser settings

**Login works locally but not in production:**

- Check authorized domains in Firebase Console
- Verify environment variables are set in Vercel

## 📚 Next Steps

After setup:

1. Test login/logout
2. Check that user data is isolated
3. Deploy to production
4. Add authorized production domains
