# Getting Started - Your Next Steps

Welcome! You now have a complete MVP for Care Companion. Here's exactly what to do next.

## What You Have

✅ **Backend (Python/FastAPI)**
- AI orchestration with Claude Sonnet 4.5
- Services for Calendar, Banking, Medications
- RESTful API with automatic documentation
- Database models ready to go

✅ **Frontend (Next.js/React)**
- Voice interface (speech recognition + synthesis)
- Chat interface with conversation history
- Large, accessible UI designed for elderly users
- Quick action buttons

✅ **Documentation**
- Complete API setup guides
- Deployment instructions
- Development best practices

## Immediate Action Plan (Next 2 Hours)

### 1. Get Anthropic API Key (5 minutes)

```bash
# Go to: https://console.anthropic.com
# Sign up → Get API key → Copy it
```

### 2. Start Backend (5 minutes)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env - minimum required:
nano .env
# Set: ANTHROPIC_API_KEY=your-key-here
# Set: DATABASE_URL=sqlite:///./noni.db
# Set: SECRET_KEY=any-random-string

# Start server
python app/main.py
```

**Test it:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### 3. Start Frontend (5 minutes)

```bash
# New terminal
cd frontend
npm install
cp .env.local.example .env.local

# Start development server
npm run dev
```

**Test it:**
- Open http://localhost:3000
- You should see the Care Companion interface

### 4. Test the AI (2 minutes)

1. Click "Type" tab
2. Type: "Hello, how are you today?"
3. Click Send
4. You should get a warm, caring response from Claude

### 5. Test Voice (2 minutes)

1. Click "Voice" tab
2. Click the microphone button (allow access)
3. Say: "What time is it?"
4. AI should respond with voice + text

**✨ If all this works, you're ready to build!**

---

## Today's Goals

### Set Up Your Development Environment

- [ ] Backend running successfully
- [ ] Frontend running successfully
- [ ] AI responding to messages
- [ ] Voice interface working
- [ ] Understand the project structure

### Read the Documentation

- [ ] README.md (main overview)
- [ ] docs/QUICKSTART.md (detailed setup)
- [ ] docs/API_SETUP_GUIDE.md (when ready for integrations)

### Customize for Your Mother

- [ ] Update AI system prompt with her name
- [ ] Test different questions she might ask
- [ ] Think about her daily routine

---

## This Week's Goals

### Day 1-2: Get Comfortable

- [ ] Run the app successfully
- [ ] Understand the AI responses
- [ ] Customize the system prompt
- [ ] Add test data (medications, events)

### Day 3-4: Set Up Database

- [ ] Sign up for Supabase (free)
- [ ] Get connection string
- [ ] Update DATABASE_URL in .env
- [ ] Test database connection

### Day 5-6: Add First Integration

Choose ONE to start:

**Option A: Calendar (Easiest)**
- [ ] Set up Google Cloud project
- [ ] Enable Calendar API
- [ ] Get OAuth credentials
- [ ] Test calendar integration

**Option B: Banking (Most Valuable)**
- [ ] Sign up for Plaid
- [ ] Get sandbox credentials
- [ ] Test with fake bank account
- [ ] Display balance in UI

### Day 7: Test & Document

- [ ] Test all features thoroughly
- [ ] Document what works
- [ ] List what needs work
- [ ] Plan next week

---

## Month 1 Roadmap

### Week 1: Foundation
- ✅ Set up local development
- ⏳ Get comfortable with code
- ⏳ Customize AI responses
- ⏳ Add test data

### Week 2: First Integration
- ⏳ Choose Calendar OR Banking
- ⏳ Complete API setup
- ⏳ Test integration
- ⏳ Show to family for feedback

### Week 3: Second Integration
- ⏳ Add the other integration
- ⏳ Add medication tracking
- ⏳ Test voice interface thoroughly
- ⏳ Refine UI based on testing

### Week 4: Deploy & Test
- ⏳ Deploy to Vercel + Railway
- ⏳ Test in production
- ⏳ Supervised testing with your mother
- ⏳ Gather feedback

---

## Working with AI Tools (Claude Code, Cursor)

### With Claude Code (This Tool!)

**Use for:**
- Backend development (Python/FastAPI)
- API integrations
- Database queries
- Debugging backend issues

**Example prompts:**
- "Add a new endpoint to get today's medications"
- "Help me integrate the Google Calendar API"
- "Debug this database connection error"
- "Add error handling to the banking service"

### With Cursor

**Use for:**
- Frontend development (React/Next.js)
- UI components
- Styling with Tailwind
- TypeScript issues

**Example prompts:**
- "Create a medication card component"
- "Add a loading spinner to the chat interface"
- "Style this button for better accessibility"
- "Fix this TypeScript error"

### Best Practices

1. **Work on one feature at a time**
2. **Test after each change**
3. **Commit to git frequently**
4. **Ask specific questions**
5. **Keep context focused**

---

## Daily Development Workflow

### Morning (Start Development)

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python app/main.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: For git, testing, etc.
cd noni
```

### During Development

```bash
# Test backend changes
curl http://localhost:8000/api/endpoint

# Test frontend
# Just refresh browser - Next.js hot reloads!

# Check logs
# Look at terminal outputs
```

### Evening (End Development)

```bash
# Commit your changes
git add .
git commit -m "Add medication reminder feature"

# Stop servers
# Press Ctrl+C in both terminals

# Deactivate Python env
deactivate
```

---

## Key Files to Know

### Backend

```
backend/
├── app/
│   ├── main.py              # ← Main FastAPI app, all routes here
│   ├── services/
│   │   ├── ai_service.py    # ← Claude AI integration
│   │   ├── calendar_service.py  # ← Google Calendar
│   │   └── banking_service.py   # ← Plaid banking
│   ├── models/
│   │   └── medication.py    # ← Database models
│   └── core/
│       ├── config.py        # ← Configuration
│       └── database.py      # ← Database setup
```

### Frontend

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx        # ← Main page
│   │   └── layout.tsx      # ← App layout
│   ├── components/
│   │   ├── ChatInterface.tsx    # ← Chat UI
│   │   ├── VoiceButton.tsx      # ← Voice UI
│   │   └── QuickActions.tsx     # ← Quick buttons
│   └── lib/
│       └── api.ts          # ← API client
```

---

## Common Tasks

### Add a New API Endpoint

1. Open `backend/app/main.py`
2. Add new route:
```python
@app.get("/api/my-new-endpoint")
async def my_endpoint():
    return {"message": "Hello!"}
```
3. Test: `curl http://localhost:8000/api/my-new-endpoint`

### Update AI Personality

1. Open `backend/app/services/ai_service.py`
2. Edit `_build_system_prompt()` method
3. Restart backend
4. Test with chat

### Add a New Component

1. Create `frontend/src/components/MyComponent.tsx`
2. Import in `page.tsx`
3. Component shows immediately (hot reload)

### Add Medication to Database

```bash
curl -X POST http://localhost:8000/api/medications \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Medicine Name",
    "dosage": "10mg",
    "frequency": "daily",
    "times": ["08:00", "20:00"],
    "user_id": 1
  }'
```

---

## Helpful Commands

### Backend

```bash
# Install new package
pip install package-name
pip freeze > requirements.txt

# Run tests
pytest

# Check Python version
python --version

# View API docs
# http://localhost:8000/docs
```

### Frontend

```bash
# Install new package
npm install package-name

# Build for production
npm run build

# Check for errors
npm run lint

# Check Node version
node --version
```

### Database

```bash
# Connect to SQLite (for quick start)
sqlite3 backend/noni.db

# View tables
.tables

# View data
SELECT * FROM medications;
```

### Git

```bash
# Check status
git status

# Commit changes
git add .
git commit -m "Description"

# Push to GitHub
git push

# View history
git log --oneline
```

---

## Resources

### Documentation
- Main README: `/noni/README.md`
- Quick Start: `/noni/docs/QUICKSTART.md`
- API Setup: `/noni/docs/API_SETUP_GUIDE.md`
- Deployment: `/noni/docs/DEPLOYMENT.md`

### APIs
- FastAPI: https://fastapi.tiangolo.com
- Next.js: https://nextjs.org/docs
- Anthropic: https://docs.anthropic.com
- Plaid: https://plaid.com/docs
- Google Calendar: https://developers.google.com/calendar

### Community
- FastAPI Discord
- Next.js Discord
- Stack Overflow (tag questions appropriately)

---

## When You Get Stuck

### 1. Check the Logs

**Backend errors:**
```bash
# Look at terminal where you ran: python app/main.py
# Errors will be printed there
```

**Frontend errors:**
```bash
# Open browser DevTools (F12)
# Go to Console tab
# Look for red errors
```

### 2. Check Environment Variables

```bash
# Backend
cd backend
cat .env
# Make sure all required variables are set

# Frontend
cd frontend
cat .env.local
# Make sure API_URL is correct
```

### 3. Restart Everything

```bash
# Stop both servers (Ctrl+C)
# Start backend
cd backend && python app/main.py

# Start frontend (new terminal)
cd frontend && npm run dev
```

### 4. Ask for Help

**Use Claude Code for:**
- Python/Backend issues
- API integration questions
- Database problems

**Use Cursor for:**
- React/Frontend issues
- UI/styling questions
- TypeScript errors

**Be specific:**
- "I'm getting this error: [paste error]"
- "I'm trying to [goal], but [what's happening]"
- "This code works in X but not in Y"

---

## You're Ready! 🚀

This is a comprehensive, production-ready foundation. Everything is:
- ✅ Structured for growth
- ✅ Designed for AI-assisted development
- ✅ Built with your mother's needs in mind
- ✅ Ready to deploy when you are

**Start with the 2-hour action plan above, then build one feature at a time.**

You've got this! 💜
