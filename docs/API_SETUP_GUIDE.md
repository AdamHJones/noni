# API Setup Guide

Complete walkthrough for obtaining all API credentials needed for Care Companion.

## Priority Order

1. **Anthropic Claude** - Required immediately ⚡
2. **Supabase/PostgreSQL** - Required immediately ⚡
3. **Google Calendar** - Setup when ready (Week 1)
4. **Plaid** - Setup when ready (Week 1-2)
5. **Twilio** - Optional for now

---

## 1. Anthropic Claude API (REQUIRED)

**Cost:** ~$10-20/month for MVP usage
**Time to setup:** 5 minutes

### Steps:

1. **Go to** https://console.anthropic.com
2. **Sign up** or log in
3. **Go to API Keys** section
4. **Create a new key**
   - Name it "Care Companion MVP"
   - Copy the key (starts with `sk-ant-`)
5. **Add to your .env file:**
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

### Testing:
```bash
cd backend
python -c "from anthropic import Anthropic; client = Anthropic(api_key='YOUR_KEY'); print('✓ Works!')"
```

### Costs:
- Claude Sonnet 4.5: ~$3 per million input tokens
- For MVP: Expect $10-20/month with moderate testing
- Production: ~$20-40/month per active user

---

## 2. Database Setup (REQUIRED)

### Option A: Supabase (Recommended for MVP)

**Cost:** Free tier is generous
**Time to setup:** 10 minutes

1. **Go to** https://supabase.com
2. **Sign up** with GitHub/Google
3. **Create new project**
   - Name: "care-companion"
   - Database password: Save this securely!
   - Region: Choose closest to you
4. **Wait 2-3 minutes** for project to provision
5. **Get connection string:**
   - Go to Project Settings → Database
   - Copy "Connection string" (URI format)
   - Replace `[YOUR-PASSWORD]` with your database password
6. **Add to .env:**
   ```
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

### Option B: Local PostgreSQL

**Cost:** Free
**Time to setup:** 15-30 minutes

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
createdb noni_db
```

**Windows:**
- Download from postgresql.org
- Run installer
- Use pgAdmin to create database

**Ubuntu/Linux:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb noni_db
```

**.env configuration:**
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/noni_db
```

---

## 3. Google Calendar API (Week 1)

**Cost:** Free
**Time to setup:** 20-30 minutes

### Steps:

1. **Go to Google Cloud Console**
   - https://console.cloud.google.com

2. **Create new project**
   - Click "Select a project" → "New Project"
   - Name: "Care Companion"
   - Click "Create"

3. **Enable APIs**
   - Go to "APIs & Services" → "Library"
   - Search for "Google Calendar API"
   - Click "Enable"
   - Also enable "Gmail API" (for future)

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Web application"
   - Name: "Care Companion Backend"

5. **Configure OAuth consent screen**
   - Click "Configure consent screen"
   - Choose "External" (unless you have workspace)
   - Fill in:
     - App name: Care Companion
     - User support email: your email
     - Developer contact: your email
   - Add scopes:
     - `../auth/calendar.readonly`
     - `../auth/calendar.events`
   - Add test users (your mother's email)

6. **Set redirect URIs**
   - Authorized redirect URIs: `http://localhost:8000/auth/google/callback`
   - For production: `https://yourdomain.com/auth/google/callback`

7. **Download credentials**
   - Click "Download JSON"
   - Save as `backend/credentials.json`

8. **Add to .env:**
   ```
   GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=xxxxx
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
   ```

### First-time authentication flow:

```python
# You'll need to run this once to get user tokens
# Instructions in backend/app/services/calendar_service.py
```

---

## 4. Plaid API (Week 1-2)

**Cost:** Free for development/sandbox, $0.30-1.00 per user/month in production
**Time to setup:** 15 minutes

### Steps:

1. **Sign up at Plaid**
   - Go to https://plaid.com/
   - Click "Get API Keys"
   - Sign up with your info

2. **Get your keys**
   - After signup, you'll see:
     - Client ID
     - Sandbox secret
     - Development secret (when ready)

3. **Add to .env:**
   ```
   PLAID_CLIENT_ID=your-client-id
   PLAID_SECRET=your-sandbox-secret
   PLAID_ENV=sandbox
   ```

### Sandbox vs Development vs Production:

- **Sandbox:** Fake data, test everything, FREE
- **Development:** Real banks, limited to 100 users, FREE
- **Production:** Real use, $0.30-1.00 per user/month

### Testing with Sandbox:

```javascript
// Use these test credentials in Plaid Link:
Username: user_good
Password: pass_good
```

### Security Notes:
- Store access tokens encrypted in production
- Never log access tokens
- Plaid tokens are read-only by default (safe!)

---

## 5. Twilio (Optional - Week 2+)

**Cost:** ~$20/month for phone number + usage
**Time to setup:** 10 minutes

### Steps:

1. **Sign up at Twilio**
   - Go to https://twilio.com
   - Sign up (they give you $15 trial credit)

2. **Get a phone number**
   - Go to Phone Numbers → Buy a Number
   - Choose a local number (~$1/month)
   - Enable SMS capability

3. **Get credentials**
   - Go to Console Dashboard
   - Copy:
     - Account SID
     - Auth Token

4. **Add to .env:**
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxx
   TWILIO_AUTH_TOKEN=your-auth-token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

### Approved Contacts:

For safety, you'll manually add approved phone numbers to the database:

```sql
INSERT INTO approved_contacts (user_id, name, phone, relationship)
VALUES (1, 'Sarah (Daughter)', '+1234567890', 'daughter');
```

---

## 6. OpenAI API (Optional)

**Cost:** ~$5-10/month
**Time to setup:** 5 minutes

Only needed if you want to use Whisper for better voice recognition (browser voice works fine for MVP).

1. **Go to** https://platform.openai.com
2. **API Keys** → Create new key
3. **Add to .env:**
   ```
   OPENAI_API_KEY=sk-xxxxx
   ```

---

## Environment Variables Checklist

Copy this to your `.env` file:

```bash
# Environment
ENVIRONMENT=development

# Database (REQUIRED)
DATABASE_URL=postgresql://user:password@localhost:5432/noni_db

# Security
SECRET_KEY=your-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Anthropic Claude API (REQUIRED)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Google APIs (Optional - add when ready)
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxx
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Plaid (Optional - add when ready)
PLAID_CLIENT_ID=xxxxx
PLAID_SECRET=xxxxx
PLAID_ENV=sandbox

# Twilio (Optional - add when ready)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+1234567890

# OpenAI (Optional)
OPENAI_API_KEY=sk-xxxxx

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Caregiver
CAREGIVER_EMAIL=your-email@example.com
CAREGIVER_PHONE=+1234567890
```

---

## Testing Your Setup

### 1. Test Backend API

```bash
cd backend
source venv/bin/activate
python app/main.py
```

Visit http://localhost:8000/docs - you should see API documentation.

### 2. Test AI Integration

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "user_id": 1,
    "conversation_history": []
  }'
```

Should return a friendly AI response.

### 3. Test Frontend

```bash
cd frontend
npm run dev
```

Visit http://localhost:3000 - you should see the voice interface.

---

## Cost Summary

**Immediate (MVP):**
- Anthropic Claude: ~$10-20/month
- Supabase: Free
- Vercel: Free
- Railway: $5/month
- **Total: $15-25/month**

**When adding features:**
- Plaid: Free (sandbox/dev)
- Twilio: ~$20/month
- **Total: $35-45/month**

**Production (per user):**
- ~$50-100/month with all features

---

## Security Best Practices

1. **Never commit .env files**
   - Already in .gitignore
   - Use .env.example as template

2. **Rotate API keys regularly**
   - Especially after testing
   - Every 90 days in production

3. **Use environment-specific keys**
   - Separate keys for dev/staging/prod
   - Never use production keys in development

4. **Encrypt sensitive data**
   - Database tokens should be encrypted
   - Use SQLAlchemy encryption or similar

5. **Monitor API usage**
   - Set up billing alerts
   - Check usage dashboards weekly

---

## Getting Help

**Anthropic Claude:**
- Docs: https://docs.anthropic.com
- Discord: https://discord.gg/anthropic

**Plaid:**
- Docs: https://plaid.com/docs
- Support: support@plaid.com

**Google Cloud:**
- Docs: https://developers.google.com
- Stack Overflow: Most issues are documented

**Supabase:**
- Docs: https://supabase.com/docs
- Discord: Active community

---

## Next Steps

1. ✅ Get Anthropic API key
2. ✅ Set up database
3. ✅ Test backend locally
4. ✅ Test frontend locally
5. → Start adding integrations one by one
6. → Deploy to production

You're ready to build! 🚀
