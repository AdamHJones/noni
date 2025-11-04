# Deployment Guide

Deploy Care Companion to production using Vercel (frontend) and Railway/Digital Ocean (backend).

## Architecture Overview

```
User → Vercel (Frontend) → Railway/DO (Backend) → External APIs
                                     ↓
                               Supabase (Database)
```

---

## Prerequisites

- [ ] GitHub account
- [ ] Vercel account (free)
- [ ] Railway account (or Digital Ocean)
- [ ] All API keys obtained
- [ ] Code tested locally

---

## Option 1: Railway (Recommended - Easiest)

**Cost:** $5/month
**Time:** 15 minutes

### Backend Deployment

1. **Push code to GitHub:**
```bash
cd /users/adamjones/noni
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/noni.git
git push -u origin main
```

2. **Deploy to Railway:**
   - Go to https://railway.app
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Select your `noni` repository
   - Railway auto-detects Python app

3. **Configure environment variables:**
   - Go to your project → Variables
   - Add all variables from your `.env` file:
     - `ANTHROPIC_API_KEY`
     - `DATABASE_URL`
     - `GOOGLE_CLIENT_ID`
     - `GOOGLE_CLIENT_SECRET`
     - `PLAID_CLIENT_ID`
     - `PLAID_SECRET`
     - etc.

4. **Set start command:**
   - Go to Settings → Deploy
   - Start command: `cd backend && python app/main.py`
   - Or use `Procfile`:
```bash
# Create Procfile in root
echo "web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

5. **Get your URL:**
   - Railway will provide: `https://your-app.up.railway.app`
   - Copy this for frontend configuration

### Frontend Deployment

1. **Deploy to Vercel:**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Vercel auto-detects Next.js

2. **Configure:**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Add environment variable:**
   - Go to Settings → Environment Variables
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
     NEXT_PUBLIC_USER_ID=1
     ```

4. **Deploy:**
   - Click "Deploy"
   - Vercel builds and deploys automatically
   - You get: `https://your-app.vercel.app`

5. **Update backend CORS:**
   - Add Vercel URL to backend allowed origins
   - In Railway, update `FRONTEND_URL` variable

---

## Option 2: Digital Ocean App Platform

**Cost:** $5-12/month
**Time:** 20 minutes

### Backend Deployment

1. **Push code to GitHub** (same as above)

2. **Create App on Digital Ocean:**
   - Go to https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Choose GitHub and select your repo
   - Select "backend" folder

3. **Configure:**
   - Name: care-companion-api
   - Region: Choose closest to you
   - Branch: main
   - Build command: `pip install -r requirements.txt`
   - Run command: `uvicorn app.main:app --host 0.0.0.0 --port 8080`

4. **Add environment variables** (same as Railway)

5. **Choose plan:**
   - Basic: $5/month
   - Professional: $12/month (more resources)

6. **Deploy:**
   - DO builds and deploys
   - You get: `https://your-app.ondigitalocean.app`

### Frontend Deployment

Same as Vercel steps above (Vercel is best for Next.js)

---

## Database Setup (Production)

### Option A: Supabase (Recommended)

Already covered in API_SETUP_GUIDE.md

1. Create project on Supabase
2. Copy connection string
3. Add to Railway/DO as `DATABASE_URL`
4. Tables auto-create on first request

### Option B: Railway PostgreSQL

1. In Railway project, click "+ New"
2. Choose "Database" → "PostgreSQL"
3. Railway creates database
4. Copy `DATABASE_URL` from database variables
5. Add to your app's variables

---

## SSL/HTTPS Configuration

**Good news:** Both Railway and Vercel provide SSL automatically!

- Vercel: Always HTTPS
- Railway: Always HTTPS
- No additional configuration needed

---

## Custom Domain (Optional)

### For Frontend (Vercel):

1. Go to Vercel project → Settings → Domains
2. Add your domain: `carecompanion.com`
3. Follow DNS configuration instructions
4. Vercel handles SSL automatically

### For Backend (Railway):

1. Go to Railway project → Settings → Domains
2. Add custom domain: `api.carecompanion.com`
3. Update DNS:
   - Type: CNAME
   - Name: api
   - Value: your-app.up.railway.app

---

## Environment Variables Checklist

### Backend (Railway/DO)

```bash
# Required
ENVIRONMENT=production
ANTHROPIC_API_KEY=sk-ant-xxxxx
DATABASE_URL=postgresql://...
SECRET_KEY=your-production-secret-key
FRONTEND_URL=https://your-app.vercel.app

# Optional (add when ready)
GOOGLE_CLIENT_ID=xxxxx
GOOGLE_CLIENT_SECRET=xxxxx
GOOGLE_REDIRECT_URI=https://your-api-url/auth/google/callback
PLAID_CLIENT_ID=xxxxx
PLAID_SECRET=xxxxx
PLAID_ENV=development  # or production
TWILIO_ACCOUNT_SID=xxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+1xxxxx
CAREGIVER_EMAIL=your@email.com
CAREGIVER_PHONE=+1xxxxx
```

### Frontend (Vercel)

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url
NEXT_PUBLIC_USER_ID=1
```

---

## Post-Deployment Checklist

### Test Basic Functionality

- [ ] Frontend loads without errors
- [ ] Can open chat interface
- [ ] AI responds to messages
- [ ] Voice button appears (may need HTTPS)
- [ ] No CORS errors in console

### Test API Endpoints

```bash
# Health check
curl https://your-backend-url/health

# Chat endpoint
curl -X POST https://your-backend-url/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","user_id":1,"conversation_history":[]}'
```

### Monitor Logs

**Railway:**
- Go to Deployments → View Logs
- Check for errors

**Vercel:**
- Go to Deployments → View Function Logs
- Check for errors

---

## Continuous Deployment

Both platforms support auto-deploy on git push:

```bash
# Make changes
git add .
git commit -m "Update AI prompt"
git push

# Railway and Vercel auto-deploy!
```

---

## Monitoring & Alerts

### Railway

1. Go to project → Observability
2. View metrics:
   - CPU usage
   - Memory usage
   - Response times

### Vercel

1. Go to project → Analytics
2. View:
   - Visitor count
   - Page load times
   - Error rates

### Set up alerts:

**Backend (Railway):**
- Settings → Notifications
- Enable email alerts for:
  - Deploy failures
  - High error rates
  - Resource limits

**Frontend (Vercel):**
- Settings → Notifications
- Enable for build failures

---

## Backup Strategy

### Database (Supabase)

- Automatic daily backups
- Go to Database → Backups
- Can restore to any point in time

### Code

- GitHub is your backup
- Tag releases:
```bash
git tag -a v0.1.0 -m "MVP release"
git push origin v0.1.0
```

---

## Security Hardening

### Backend

1. **Rotate secrets:**
```bash
# Generate new SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Update CORS:**
```python
# In app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. **Rate limiting:**
```python
# Add to requirements.txt
slowapi==0.1.9

# Add to app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(...):
    ...
```

### Frontend

1. **Environment variables:**
   - Only use `NEXT_PUBLIC_` for truly public values
   - Never expose API keys in frontend

2. **Content Security Policy:**
```javascript
// next.config.js
const securityHeaders = [
  {
    key: 'X-Frame-Options',
    value: 'DENY',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
]

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ]
  },
}
```

---

## Costs Summary

### Development/Testing

- Vercel: Free
- Railway: Free (with $5 credit)
- Supabase: Free
- **Total: $0**

### Production (MVP)

- Vercel: Free (hobby plan)
- Railway: $5/month
- Supabase: Free (or $25/month for more)
- Anthropic: ~$20/month
- **Total: ~$25-50/month**

### Production (Full Features)

- Vercel: Free
- Railway: $5-20/month (depending on usage)
- Supabase: $25/month
- Anthropic: ~$30-50/month
- Plaid: $30-50/month
- Twilio: $20/month
- **Total: ~$110-165/month**

---

## Rollback Strategy

### If deployment breaks:

**Railway:**
```bash
# In Railway dashboard
Deployments → Click previous working deployment → Redeploy
```

**Vercel:**
```bash
# In Vercel dashboard
Deployments → Find working deployment → Promote to Production
```

**Git:**
```bash
# Revert last commit
git revert HEAD
git push

# Or rollback to specific version
git reset --hard v0.1.0
git push --force
```

---

## Troubleshooting Production Issues

### Backend not responding

1. **Check logs** (Railway/DO dashboard)
2. **Check environment variables** are all set
3. **Check database connection** (test DATABASE_URL)
4. **Check API keys** are valid

### Frontend can't reach backend

1. **Check NEXT_PUBLIC_API_URL** is correct
2. **Check CORS settings** in backend
3. **Check backend is running** (visit /health endpoint)
4. **Check browser console** for CORS errors

### Database errors

1. **Check DATABASE_URL** format
2. **Check Supabase** is running (supabase.com status)
3. **Check tables exist** (should auto-create)
4. **Check connection limits** (upgrade plan if needed)

---

## Next Steps After Deployment

1. **Test thoroughly** with real usage
2. **Monitor logs** for first few days
3. **Set up error tracking** (Sentry, LogRocket)
4. **Configure monitoring** (UptimeRobot)
5. **Enable backups** (automated)
6. **Document for team** (if applicable)
7. **Train users** (your mother, caregivers)

---

## Production Checklist

Before going live:

- [ ] All API keys are production keys
- [ ] Database has backups enabled
- [ ] CORS is configured properly
- [ ] SSL/HTTPS is working
- [ ] Error logging is set up
- [ ] Monitoring is configured
- [ ] Custom domain (if using)
- [ ] Tested all critical features
- [ ] Have rollback plan
- [ ] Caregiver has access

---

## Support

**Railway:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**Vercel:**
- Docs: https://vercel.com/docs
- Support: support@vercel.com

**Supabase:**
- Docs: https://supabase.com/docs
- Discord: Community support

You're ready to deploy! 🚀
