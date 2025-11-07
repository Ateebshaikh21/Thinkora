# ⚠️ Git Not Installed - Install It First!

## 🔧 Install Git on Windows

### Option 1: Download Git Installer (Recommended)

1. **Download Git:**

   - Go to: https://git-scm.com/download/win
   - Click "Click here to download" (64-bit version)
   - File will be named: `Git-2.43.0-64-bit.exe` (or similar)

2. **Run the Installer:**

   - Double-click the downloaded file
   - Click "Next" through the installation
   - **Important:** Keep all default settings
   - Click "Install"
   - Click "Finish"

3. **Verify Installation:**
   - Close and reopen PowerShell
   - Run: `git --version`
   - You should see: `git version 2.43.0` (or similar)

### Option 2: Install via Winget (Windows Package Manager)

If you have Windows 11 or Windows 10 (recent version):

```powershell
winget install --id Git.Git -e --source winget
```

### Option 3: Install via Chocolatey

If you have Chocolatey installed:

```powershell
choco install git
```

---

## ✅ After Installing Git

**Close and reopen PowerShell**, then run:

```powershell
git --version
```

If you see a version number, Git is installed! ✅

---

## 🚀 Then Continue with Deployment

Once Git is installed, run these commands:

```powershell
# Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
git init
git add .
git commit -m "Initial commit - Thinkora AI Study Assistant"
```

Then follow the rest of the steps in `DEPLOY_NOW.md`

---

## 🆘 Alternative: Use GitHub Desktop (No Git Command Line Needed)

If you prefer a GUI instead of command line:

1. **Download GitHub Desktop:**

   - Go to: https://desktop.github.com
   - Download and install

2. **Use GitHub Desktop:**

   - Open GitHub Desktop
   - Click "Add" → "Add Existing Repository"
   - Select your Thinkora folder
   - Click "Publish repository" to GitHub
   - Follow the prompts

3. **Then deploy:**
   - Continue with Render and Vercel deployment from `DEPLOY_NOW.md`

---

## 📝 Quick Summary

**You need to:**

1. Install Git (5 minutes)
2. Close and reopen PowerShell
3. Run git commands
4. Continue with deployment

**Download Git here:** https://git-scm.com/download/win

---

After installing Git, come back and follow `DEPLOY_NOW.md`! 🚀
