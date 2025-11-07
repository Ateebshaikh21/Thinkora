# 🚀 Thinkora Deployment Guide

## Overview

Thinkora consists of two parts:

- **Frontend:** React + Vite application
- **Backend:** Python FastAPI server

You can deploy them separately or together. Here are your options:

---

## 📋 Pre-Deployment Checklist

### 1. Environment Variables

Create production environment files:

**Backend (`backend/.env`):**

```env
# MongoDB (if using)
MONGODB_URL=your_mongodb_connection_string

# OpenAI API (if using)
OPENAI_API_KEY=your_openai_api_key

# Server Configuration
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production

# CORS Origins (update with your frontend URL)
CORS_ORIGINS=https://your-frontend-domain.com
```

**Frontend (`.env.production`):**

```env
VITE_API_URL=https://your-backend-domain.com/api
```

### 2. Update API URLs

Update `frontend/src/` files to use environment variable:

```javascript
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
```

---

## 🎯 Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend) ⭐ RECOMMENDED

**Best for:** Quick deployment, free tier available, easy setup

#### Deploy Backend to Render:

1. **Create account:** https://render.com
2. **Create New Web Service**
3. **Connect GitHub repository**
4. **Configure:**
   ```
   Name: thinkora-backend
   Environment: Python 3
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. **Add Environment Variables** (from .env above)
6. **Deploy!**

#### Deploy Frontend to Vercel:

1. **Create account:** https://vercel.com
2. **Import Git Repository**
3. **Configure:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```
4. **Add Environment Variable:**
   ```
   VITE_API_URL=https://your-render-backend.onrender.com/api
   ```
5. **Deploy!**

**Cost:** Free tier available for both!

---

### Option 2: Railway (Full Stack) 🚂

**Best for:** Simple full-stack deployment, one platform

1. **Create account:** https://railway.app
2. **New Project → Deploy from GitHub**
3. **Add two services:**

**Backend Service:**

```
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Frontend Service:**

```
Root Directory: frontend
Build Command: npm install && npm run build
Start Command: npm run preview
```

4. **Add environment variables**
5. **Deploy!**

**Cost:** $5/month after free trial

---

### Option 3: AWS (Production-Ready) ☁️

**Best for:** Scalable production deployment

#### Backend on AWS Elastic Beanstalk:

1. **Install AWS CLI and EB CLI:**

```bash
pip install awsebcli
```

2. **Initialize:**

```bash
cd backend
eb init -p python-3.11 thinkora-backend
```

3. **Create environment:**

```bash
eb create thinkora-prod
```

4. **Deploy:**

```bash
eb deploy
```

#### Frontend on AWS S3 + CloudFront:

1. **Build frontend:**

```bash
cd frontend
npm run build
```

2. **Create S3 bucket:**

```bash
aws s3 mb s3://thinkora-frontend
```

3. **Upload:**

```bash
aws s3 sync dist/ s3://thinkora-frontend --acl public-read
```

4. **Setup CloudFront** for CDN and HTTPS

**Cost:** Pay-as-you-go, ~$10-50/month

---

### Option 4: DigitalOcean (VPS) 💧

**Best for:** Full control, custom configuration

1. **Create Droplet** (Ubuntu 22.04, $6/month)

2. **SSH into server:**

```bash
ssh root@your-droplet-ip
```

3. **Install dependencies:**

```bash
# Update system
apt update && apt upgrade -y

# Install Python
apt install python3-pip python3-venv -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install nodejs -y

# Install Nginx
apt install nginx -y
```

4. **Clone repository:**

```bash
git clone https://github.com/yourusername/thinkora.git
cd thinkora
```

5. **Setup Backend:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
nano /etc/systemd/system/thinkora-backend.service
```

**Service file:**

```ini
[Unit]
Description=Thinkora Backend
After=network.target

[Service]
User=root
WorkingDirectory=/root/thinkora/backend
Environment="PATH=/root/thinkora/backend/venv/bin"
ExecStart=/root/thinkora/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable thinkora-backend
systemctl start thinkora-backend
```

6. **Setup Frontend:**

```bash
cd ../frontend
npm install
npm run build
```

7. **Configure Nginx:**

```bash
nano /etc/nginx/sites-available/thinkora
```

**Nginx config:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /root/thinkora/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/thinkora /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

8. **Setup SSL with Let's Encrypt:**

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

**Cost:** $6/month + domain

---

### Option 5: Docker + Any Cloud 🐳

**Best for:** Containerized deployment, portability

1. **Create `Dockerfile` for backend:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Create `Dockerfile` for frontend:**

```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

3. **Create `docker-compose.yml`:**

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=${MONGODB_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
      - ./sessions:/app/sessions
      - ./quiz_results:/app/quiz_results

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://backend:8000/api
```

4. **Deploy:**

```bash
docker-compose up -d
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure CORS properly
- [ ] Set up environment variables (never commit .env)
- [ ] Enable rate limiting
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Use strong API keys
- [ ] Enable logging and monitoring
- [ ] Set up error tracking (Sentry)

---

## 📊 Monitoring & Maintenance

### Recommended Tools:

1. **Uptime Monitoring:** UptimeRobot (free)
2. **Error Tracking:** Sentry (free tier)
3. **Analytics:** Google Analytics or Plausible
4. **Logs:** Papertrail or Logtail

### Backup Strategy:

1. **Database:** Daily automated backups
2. **User Data:** Weekly backups of sessions and quiz results
3. **Code:** Git repository (already done!)

---

## 💰 Cost Comparison

| Option          | Monthly Cost | Difficulty | Best For          |
| --------------- | ------------ | ---------- | ----------------- |
| Vercel + Render | Free - $20   | Easy       | Getting started   |
| Railway         | $5 - $20     | Easy       | Simple deployment |
| AWS             | $10 - $100+  | Medium     | Scalability       |
| DigitalOcean    | $6 - $50     | Medium     | Full control      |
| Docker          | Varies       | Medium     | Flexibility       |

---

## 🚀 Quick Start (Recommended)

**For beginners, start with Vercel + Render:**

1. Push code to GitHub
2. Deploy backend to Render (5 minutes)
3. Deploy frontend to Vercel (5 minutes)
4. Update environment variables
5. Done! ✅

**Total time:** ~15 minutes  
**Cost:** Free tier available

---

## 📝 Post-Deployment

After deployment:

1. **Test all features:**

   - Document upload
   - Question analysis
   - Quiz generation
   - Quiz submission
   - History tracking

2. **Update DNS** (if using custom domain)

3. **Monitor logs** for errors

4. **Set up analytics**

5. **Share with users!** 🎉

---

## 🆘 Troubleshooting

### Common Issues:

**CORS Errors:**

- Update `CORS_ORIGINS` in backend
- Check API URL in frontend

**API Not Found:**

- Verify backend URL in frontend env
- Check backend is running

**Build Failures:**

- Check Node/Python versions
- Verify all dependencies installed

**Database Connection:**

- Check MongoDB connection string
- Verify network access

---

## 📚 Additional Resources

- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [AWS Docs](https://docs.aws.amazon.com)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)

---

**Need help?** Check the logs, read error messages, and don't hesitate to ask! 🚀

Good luck with your deployment! 🎓✨
