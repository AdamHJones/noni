# Week One Deployment Plan
## Get Your Mother Using Care Companion in 3 Days

**Goal**: Deploy to production, set up for your mother, test on her iPhone

**Your Commitment**: Hybrid approach
- Help mother NOW (this week)
- Validate and refine (next 30 days)
- Expand to small platform if successful (months 2-4)
- Scale to full marketplace if traction (months 5-12)

---

## Pre-Deployment Checklist

Before we start, make sure you have:
- ✅ Code on GitHub (done - https://github.com/AdamHJones/noni)
- ✅ Computer with terminal access (you have this)
- ✅ Credit card for API keys (free tiers available)
- ✅ Your mother's iPhone available for testing
- ⏳ 2-3 hours for deployment (spread over 2-3 days)

---

## Day 1: Get API Keys & Deploy Backend (2 hours)

### Step 1: Get Anthropic API Key (15 minutes)

**Why**: Powers the AI assistant and vision analysis

**How**:
1. Go to https://console.anthropic.com/
2. Sign up with your email (if you don't have account)
3. Go to "API Keys" in dashboard
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)
6. **Save it somewhere safe** (you'll need it in a minute)

**Cost**:
- $5 credit to start (free)
- Then pay-as-you-go (~$7-15/month with typical use)
- Your mother's usage should be ~$10/month

**Test it works**:
```bash
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY_HERE" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Say hello!"}]
  }'
```

If you see a response, it's working!

---

### Step 2: Deploy Backend to Railway (30 minutes)

**Why**: Railway gives you free PostgreSQL + hosting (free tier = $5/month credit)

**How**:

1. **Sign up for Railway**:
   - Go to https://railway.app/
   - Sign up with GitHub (it will connect to your repos)
   - Verify your email

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose "AdamHJones/noni"
   - Railway will detect it's a Python app

3. **Configure for Backend**:
   - Railway might try to deploy the whole repo
   - We need to tell it to deploy from the `backend` folder
   - In project settings:
     - Root Directory: `/backend`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add PostgreSQL Database**:
   - In your Railway project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will create database and give you connection URL

5. **Set Environment Variables**:

   In Railway project settings, add these variables:

   ```bash
   # Required
   ANTHROPIC_API_KEY=sk-ant-xxx... (your key from Step 1)
   DATABASE_URL=(automatically set by Railway when you added PostgreSQL)

   # Optional for now (can add later)
   # GOOGLE_CLIENT_ID=
   # GOOGLE_CLIENT_SECRET=
   # PLAID_CLIENT_ID=
   # PLAID_SECRET=
   # TWILIO_ACCOUNT_SID=
   # TWILIO_AUTH_TOKEN=
   # TWILIO_PHONE_NUMBER=

   # Set these
   SECRET_KEY=your-secret-key-here-make-it-random-and-long
   CORS_ORIGINS=*
   ```

   For `SECRET_KEY`, generate a random string:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

6. **Deploy**:
   - Railway will auto-deploy
   - Wait 2-3 minutes for build
   - You'll get a URL like: `https://noni-backend-production.up.railway.app`

7. **Test Backend**:
   - Open: `https://your-railway-url.railway.app/docs`
   - You should see FastAPI documentation
   - Try the `/health` endpoint - should return `{"status": "healthy"}`

**If it fails**:
- Check Railway logs (click on deployment, view logs)
- Common issues:
  - Missing environment variables
  - Database connection issues
  - Python dependency conflicts

**Cost**:
- Railway: $5/month credit (free effectively)
- PostgreSQL: Included in free tier

---

### Step 3: Initialize Database (10 minutes)

**Problem**: Database is empty, we need to create tables

**Solution**: Railway gives you a way to run commands

1. **Option A - Railway Shell**:
   - In Railway, open your backend service
   - Click "Shell" tab
   - Run:
   ```bash
   python -c "from app.core.database import engine; from app.models.medication import Base; Base.metadata.create_all(bind=engine)"
   ```

2. **Option B - Local script to remote DB**:
   - Copy the `DATABASE_URL` from Railway
   - Run locally:
   ```bash
   cd backend
   export DATABASE_URL="postgresql://..." (paste from Railway)
   python3 -c "from app.core.database import engine; from app.models.medication import Base; Base.metadata.create_all(bind=engine)"
   ```

**Verify**:
- Go to Railway → PostgreSQL service → Data tab
- You should see tables: users, patients, caregivers, medications, etc.

---

## Day 2: Deploy Frontend & Connect (1 hour)

### Step 4: Deploy Frontend to Vercel (20 minutes)

**Why**: Vercel is perfect for Next.js (free tier, auto HTTPS)

**How**:

1. **Sign up for Vercel**:
   - Go to https://vercel.com/
   - Sign up with GitHub
   - Authorize Vercel to access your repos

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Select "AdamHJones/noni" repo
   - Vercel will detect Next.js

3. **Configure Frontend**:
   - Framework Preset: Next.js (auto-detected)
   - Root Directory: `/frontend`
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

4. **Set Environment Variables**:

   In Vercel project settings → Environment Variables:

   ```bash
   NEXT_PUBLIC_API_URL=https://your-railway-backend-url.railway.app
   ```

   Replace with your actual Railway backend URL from Step 2.

5. **Deploy**:
   - Click "Deploy"
   - Wait 1-2 minutes
   - Vercel gives you URL like: `https://noni.vercel.app`
   - Also generates URLs like: `https://noni-git-main-adamhjones.vercel.app`

6. **Test Frontend**:
   - Open your Vercel URL
   - You should see the Care Companion home screen
   - Big microphone button in center
   - Quick action buttons below

**If voice doesn't work yet**:
- Normal! Voice requires HTTPS (you have it) + user interaction
- We'll test on iPhone in next step

**Cost**:
- Vercel: 100% FREE (hobby plan)

---

### Step 5: Connect Frontend to Backend (10 minutes)

**Test the connection**:

1. **Open browser console**:
   - Open your Vercel URL
   - Right-click → Inspect → Console tab

2. **Check for errors**:
   - If you see CORS errors, we need to fix backend
   - Go back to Railway backend environment variables
   - Update `CORS_ORIGINS`:
   ```bash
   CORS_ORIGINS=https://noni.vercel.app,https://noni-git-main-adamhjones.vercel.app
   ```
   - Railway will auto-redeploy

3. **Test AI Chat**:
   - On your app home screen, click "Quick Actions" → "What's today?"
   - AI should respond with current date
   - Check console for any errors

**If chat doesn't work**:
- Check Network tab in browser console
- Look for failed requests to `/api/chat`
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Check Railway logs for backend errors

---

### Step 6: Update Backend CORS (5 minutes)

**Why**: Backend needs to allow requests from your Vercel domain

**How**:

Open `backend/app/main.py` and verify CORS is set up:

```python
# Should already be there, but verify:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

And in Railway environment variables:
```bash
CORS_ORIGINS=https://noni.vercel.app,https://noni-git-main-adamhjones.vercel.app,http://localhost:3000
```

(Include localhost for local testing)

---

## Day 3: Set Up for Your Mother (1 hour)

### Step 7: Create User Accounts (15 minutes)

**We need**:
1. Your mother's patient account
2. Your family admin account
3. (Later) Caregiver account when you hire someone

**Option A - Via Database** (Recommended for now):

Create a quick script: `backend/create_initial_users.py`

```python
import asyncio
from app.core.database import SessionLocal
from app.models.medication import User, Patient, FamilyAdmin, PatientFamilyRelationship
from datetime import date

async def create_users():
    db = SessionLocal()

    try:
        # 1. Create your mother as patient
        patient_user = User(
            email="dorothy@example.com",  # Use a real email if she has one
            password_hash="temporary",  # She'll use voice, won't need login
            role="patient",
            first_name="Dorothy",
            last_name="Martinez",  # Use your mother's actual name
            phone="(415) 555-0123",  # Her actual phone
            email_verified=True
        )
        db.add(patient_user)
        db.commit()
        db.refresh(patient_user)

        # Create patient profile
        patient = Patient(
            user_id=patient_user.id,
            date_of_birth=date(1947, 3, 15),  # Her actual DOB
            diagnosis="Early-stage Alzheimer's disease",  # Adjust as needed
            care_level=2,  # 0-4 scale
            primary_address="123 Oak Street, San Francisco, CA",  # Her address
            language_preference="en",
            voice_preference="Samantha",
            location_tracking_enabled=True
        )
        db.add(patient)
        db.commit()

        # 2. Create your admin account
        admin_user = User(
            email="your-email@example.com",  # YOUR email
            password_hash="temporary",  # We'll add proper auth later
            role="family_admin",
            first_name="Sarah",  # Your name
            last_name="Martinez",
            phone="(415) 555-0199",  # Your phone
            email_verified=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        # Create family admin profile
        family_admin = FamilyAdmin(
            user_id=admin_user.id,
            relationship_type="daughter"  # or "son", "spouse", etc.
        )
        db.add(family_admin)
        db.commit()
        db.refresh(family_admin)

        # 3. Link you to your mother
        relationship = PatientFamilyRelationship(
            patient_id=patient.id,
            family_admin_id=family_admin.id,
            permission_level="full_admin",
            is_primary=True
        )
        db.add(relationship)
        db.commit()

        print(f"✅ Created patient: {patient_user.email} (ID: {patient_user.id})")
        print(f"✅ Created admin: {admin_user.email} (ID: {admin_user.id})")
        print(f"✅ Linked relationship")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(create_users())
```

**Run it**:
```bash
cd backend
export DATABASE_URL="your-railway-database-url"
python3 create_initial_users.py
```

**Option B - Via API** (We'll add this later):
- Create a `/api/setup` endpoint
- Call it once to initialize

---

### Step 8: Add Her Medications (15 minutes)

Create another script: `backend/add_medications.py`

```python
from app.core.database import SessionLocal
from app.models.medication import Medication
from datetime import date

def add_medications():
    db = SessionLocal()

    try:
        # Get your mother's patient ID (from previous step output)
        patient_id = 1  # Replace with actual ID

        medications = [
            {
                "patient_id": patient_id,
                "name": "Donepezil",
                "dosage": "10mg",
                "frequency": "Once daily",
                "time_of_day": "Morning",
                "schedule": {"times": ["09:00"], "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
                "prescribing_doctor": "Dr. Anderson",
                "pharmacy": "Walgreens #4521",
                "instructions": "Take with breakfast",
                "active": True,
                "start_date": date.today()
            },
            {
                "patient_id": patient_id,
                "name": "Lisinopril",
                "dosage": "20mg",
                "frequency": "Once daily",
                "time_of_day": "Morning",
                "schedule": {"times": ["09:00"], "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
                "prescribing_doctor": "Dr. Johnson",
                "pharmacy": "Walgreens #4521",
                "instructions": "Take with water",
                "active": True,
                "start_date": date.today()
            },
            # Add more as needed
        ]

        for med_data in medications:
            med = Medication(**med_data)
            db.add(med)

        db.commit()
        print(f"✅ Added {len(medications)} medications")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_medications()
```

**Run it**:
```bash
python3 add_medications.py
```

---

### Step 9: Test on iPhone (20 minutes)

**Time to see if it works!**

1. **Open on iPhone**:
   - Open Safari on your mother's iPhone
   - Go to your Vercel URL: `https://noni.vercel.app`
   - You should see the app

2. **Install as PWA**:
   - Tap the "Share" button (box with arrow up)
   - Scroll down, tap "Add to Home Screen"
   - Tap "Add"
   - You'll see "Care Companion" icon on home screen

3. **Grant Permissions**:
   - Tap the app icon to open
   - When prompted, allow:
     - ✅ Microphone access (for voice)
     - ✅ Camera access (for photo analysis)
     - ✅ Location access → "Allow While Using App" or "Always Allow"

4. **Test Voice**:
   - Tap the big microphone button
   - Say "What time is it?"
   - AI should respond with current time
   - Voice should play automatically

5. **Test Camera**:
   - Tap "Camera" icon at bottom
   - Select "Medication Label"
   - Take photo of a pill bottle
   - Should analyze and show results in 3-5 seconds

6. **Test Location**:
   - Tap "Share Location" button
   - Should show current location
   - You (as admin) should be able to see it

**Common Issues**:

**Voice not working**:
- Must be HTTPS (you have this via Vercel ✓)
- Must grant microphone permission
- Try Safari (not Chrome) on iPhone
- Restart app

**Camera not working**:
- Grant camera permission in Settings → Care Companion
- Make sure good lighting
- Hold phone steady

**Location not working**:
- Grant location permission (Always Allow recommended)
- Enable Location Services in iPhone Settings
- May take 30 seconds to get first location

---

### Step 10: Configure Settings (10 minutes)

**Customize for your mother**:

For now, we'll do this directly in the database. Later we'll add a UI for you to change these.

Connect to Railway PostgreSQL:
1. Railway dashboard → PostgreSQL service → Data tab
2. Or use a tool like TablePlus, pgAdmin

**Key settings to adjust**:

**In `patients` table** (your mother's row):
- `voice_preference`: "Samantha" (or another iOS voice)
- `ai_personality_settings`:
  ```json
  {
    "speed": 0.85,
    "formality": "warm",
    "repetition_handling": "patient",
    "reading_level": "5th_grade"
  }
  ```
- `location_tracking_enabled`: `true`

**Add a geofence** (in `geofences` table):
```sql
INSERT INTO geofences (patient_id, name, center_lat, center_lng, radius_meters, alert_on_exit, active_hours, notify_users)
VALUES (
  1,  -- your mother's patient_id
  'Home',
  37.7749,  -- her actual latitude
  -122.4194,  -- her actual longitude
  100,  -- 100 meter radius
  true,  -- alert when she leaves
  '{"start": "22:00", "end": "06:00"}',  -- only alert at night
  ARRAY[2]  -- your admin user_id
);
```

To get her exact coordinates:
- Go to Google Maps
- Find her address
- Right-click → "What's here?"
- Copy lat/lng

---

## Day 4-7: Monitor & Refine

### Step 11: Watch Usage (Ongoing)

**Things to monitor**:

1. **Is she using it?**
   - Check `ai_conversations` table for entries
   - Are there new conversations daily?

2. **What's she asking?**
   - Review conversation transcripts
   - Look for patterns
   - Identify confusion points

3. **Are there errors?**
   - Check Railway logs (backend)
   - Check Vercel logs (frontend)
   - Check browser console on her iPhone

4. **Is she getting value?**
   - Talk to her: "How do you like the app?"
   - Is she calmer? More independent?
   - Does she reach for it when confused?

---

### Step 12: Quick Fixes

**Likely issues in first week**:

**"Voice is too fast"**:
- Adjust in `VoiceButton.tsx`: `utterance.rate = 0.7` (slower)
- Or update patient settings: `ai_personality_settings.speed = 0.7`

**"She keeps asking the same question"**:
- This is expected with Alzheimer's
- AI is designed to patiently repeat
- Monitor if it's handling gracefully

**"Voice doesn't sound natural"**:
- Try different iOS voices
- Update `voice_preference` in patient settings
- Options: "Samantha", "Karen", "Victoria", "Alex"

**"She doesn't know how to use it"**:
- Simplify home screen (reduce buttons)
- Make voice button even bigger
- Add voice prompt: "Say 'Help' to learn what I can do"

**"Battery drains fast"**:
- Location tracking can drain battery
- Reduce update frequency
- Set to "Significant Location Change" mode

---

### Step 13: Onboard First Caregiver (When Ready)

**When you hire a caregiver for your mother**:

1. **Create caregiver account**:

   Similar to patient creation, but:
   ```python
   caregiver_user = User(
       email="sarah.k@example.com",
       password_hash="temporary",  # They'll set password
       role="caregiver",
       first_name="Sarah",
       last_name="K",
       phone="(415) 555-1234"
   )

   caregiver = Caregiver(
       user_id=caregiver_user.id,
       certification_level=2,  # Dementia care specialist
       years_experience=8,
       hourly_rate=25.00,
       specializations=["dementia", "alzheimers"],
       has_car=True,
       willing_to_transport=True
   )
   ```

2. **Create care assignment**:
   ```python
   assignment = CareAssignment(
       patient_id=1,  # your mother
       caregiver_id=caregiver.id,
       status="active",
       start_date=date.today(),
       recurring_schedule={
           "mon": "09:00-12:00",
           "wed": "09:00-12:00",
           "fri": "09:00-12:00"
       },
       hourly_rate=25.00,
       care_plan="Help with morning routine, medication reminders, light meal prep",
       created_by=2  # your admin user_id
   )
   ```

3. **Show caregiver the app**:
   - Give them the Vercel URL
   - They log in (we need to add login UI, or give them direct access)
   - Show them how to:
     - Clock in/out
     - Log medication given (with photo)
     - Add session notes
     - Report concerns

4. **Monitor caregiver activity**:
   - Check `care_sessions` table for logged sessions
   - Review notes and photos
   - Ensure they're completing tasks

---

## Success Metrics (First 30 Days)

**Track these to decide whether to expand**:

### Usage Metrics
- [ ] Mother uses app daily (3+ interactions/day)
- [ ] Voice interface works reliably (>90% success rate)
- [ ] She finds it helpful (ask her weekly)
- [ ] Reduces calls to you for basic questions

### Technical Metrics
- [ ] Uptime >99% (check Railway/Vercel status)
- [ ] Response time <2 seconds for AI
- [ ] No critical errors (check logs)
- [ ] Camera/location features work

### Care Quality Metrics
- [ ] Medication adherence improves (track in `medication_logs`)
- [ ] You have visibility into her day (via activity logs)
- [ ] Caregiver logging is consistent
- [ ] No safety incidents (wandering, missed meds)

### Business Validation (If expanding)
- [ ] Friends/family express interest ("I want this for my parent!")
- [ ] Caregiver likes using it (would recommend to others)
- [ ] You feel confident it could scale
- [ ] Willing to invest time/money to expand

---

## Cost Tracking (First Month)

**Expected costs**:

| Service | Cost |
|---------|------|
| Anthropic API (Claude) | ~$10-15 |
| Railway (Backend + DB) | $5 |
| Vercel (Frontend) | $0 (free) |
| **Total** | **$15-20/month** |

**If you add**:
- Google Calendar: $0 (free tier)
- Plaid (banking): $0 (sandbox) or $5/month
- Twilio (SMS): $1-5/month
- **Total with extras**: **$20-30/month**

Still incredibly cheap for what you get!

---

## Week 2-4 Roadmap

### Week 2: Stability & Refinement
- Fix any bugs discovered in Week 1
- Adjust AI prompts based on conversations
- Optimize voice settings
- Add any missing medications
- Fine-tune location/geofencing

### Week 3: Caregiver Onboarding
- Add your first caregiver
- Train them on the app
- Monitor their logging
- Ensure communication flow works

### Week 4: Decision Point
- Review success metrics
- Talk to mother: Is it helping?
- Talk to caregiver: Would you recommend it?
- Decide: Keep personal OR expand to friends?

---

## If Expanding (Month 2+)

**Signs you should expand**:
✅ Mother loves it, uses it daily
✅ Caregiver finds it valuable
✅ You've had 3+ people say "I want this for my parent"
✅ No major technical issues
✅ You have 10-15 hours/week to commit

**Next steps**:
1. **Add authentication** (proper login system)
2. **Build family dashboard** (web interface for you)
3. **Add 2-3 beta families** (friends/family)
4. **Integrate Stripe** (automated payments)
5. **Simple marketplace** (families can pick from caregivers you approve)

**Cost**: $5k-10k if you hire contractor, or build yourself with AI tools

**Timeline**: 2-3 months to small platform (Option B)

---

## Troubleshooting

### Backend Issues

**"Railway deployment failed"**:
- Check logs in Railway dashboard
- Common fix: Add missing environment variables
- Ensure `requirements.txt` is complete

**"Database connection error"**:
- Verify `DATABASE_URL` is set in Railway
- Check PostgreSQL service is running
- Try restarting backend service

**"API requests failing"**:
- Check CORS settings
- Verify `ANTHROPIC_API_KEY` is set
- Look at Railway logs for errors

### Frontend Issues

**"Vercel deployment failed"**:
- Check build logs
- Ensure `NEXT_PUBLIC_API_URL` is set
- Try deploying from `main` branch

**"Voice not working on iPhone"**:
- Must be HTTPS (Vercel provides this ✓)
- User must interact first (tap button)
- Check Safari, not Chrome
- Enable microphone in Settings

**"Camera not working"**:
- Grant camera permission
- Ensure good lighting
- Try taking photo from gallery first

### Database Issues

**"Tables don't exist"**:
- Run database initialization (Step 3)
- Check Railway PostgreSQL is provisioned
- Verify connection string

**"Can't connect to database"**:
- Get connection string from Railway
- Check if database is running
- Firewall/network issues (unlikely with Railway)

---

## Quick Reference

### Important URLs
- **Backend**: https://your-app.railway.app
- **Frontend**: https://noni.vercel.app
- **GitHub**: https://github.com/AdamHJones/noni
- **Railway Dashboard**: https://railway.app/dashboard
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Anthropic Console**: https://console.anthropic.com/

### Environment Variables

**Backend (Railway)**:
```
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=(auto-set by Railway)
SECRET_KEY=(random string)
CORS_ORIGINS=https://noni.vercel.app
```

**Frontend (Vercel)**:
```
NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app
```

### Key Commands

**Test backend locally**:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Test frontend locally**:
```bash
cd frontend
npm run dev
```

**Database operations**:
```bash
# Initialize tables
python3 -c "from app.core.database import engine; from app.models.medication import Base; Base.metadata.create_all(bind=engine)"

# Check Railway logs
railway logs -s backend
```

---

## Need Help?

**If you get stuck**:
1. Check Railway/Vercel logs first
2. Review error messages carefully
3. Ask me! I can help debug

**Common questions**:
- "How do I add more medications?" → Update database or wait for UI
- "How do I change AI voice?" → Update patient settings
- "How do I see conversation logs?" → Query `ai_conversations` table
- "How much is this costing?" → Check Anthropic console + Railway usage

---

## Next: Month 2 Planning

After 30 days of your mother using it, we'll:
1. Review success metrics
2. Gather detailed feedback
3. Decide: Stay personal or expand?
4. If expanding: Plan Option B features
5. If staying: Keep refining for her needs

**Either way, you've built something amazing that helps your mother NOW.**

---

**Ready to deploy?**

Start with **Day 1, Step 1** above. I'll help you through each step!
