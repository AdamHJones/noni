# Quick Start Guide (15 Minutes)

Get Care Companion running locally in 15 minutes.

## Prerequisites Checklist

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Git installed
- [ ] Text editor (VS Code, Cursor, etc.)

---

## Step 1: Get Anthropic API Key (5 min)

1. Go to https://console.anthropic.com
2. Sign up or log in
3. Create new API key
4. Copy the key (starts with `sk-ant-`)
5. Save it somewhere safe

---

## Step 2: Setup Backend (5 min)

```bash
# Navigate to backend
cd /users/adamjones/noni/backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file and add your Anthropic key
# Use nano, vim, or your text editor:
nano .env

# Set these minimum required values:
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# DATABASE_URL=sqlite:///./noni.db  # SQLite for quick start
# SECRET_KEY=any-random-string-here

# Run the server
python app/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!**

---

## Step 3: Setup Frontend (5 min)

Open a NEW terminal window:

```bash
# Navigate to frontend
cd /users/adamjones/noni/frontend

# Install dependencies
npm install

# Create .env file
cp .env.local.example .env.local

# No changes needed for local development!

# Run the development server
npm run dev
```

You should see:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## Step 4: Test It! (2 min)

1. **Open your browser:** http://localhost:3000

2. **You should see:**
   - "Care Companion" header
   - Voice/Type tabs
   - Large microphone button

3. **Test the chat interface:**
   - Click "Type" tab
   - Type: "Hello, how are you?"
   - Press Send
   - You should get a warm, friendly AI response

4. **Test voice (Chrome/Safari only):**
   - Click "Voice" tab
   - Click the microphone button
   - Allow microphone access
   - Say: "What time is it?"
   - AI should respond with voice + text

---

## ✅ Success Checklist

If everything works, you should have:
- [x] Backend running on port 8000
- [x] Frontend running on port 3000
- [x] AI responding to chat messages
- [x] Voice interface working (in supported browsers)

---

## 🐛 Troubleshooting

### Backend won't start

**Error: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Error: "ANTHROPIC_API_KEY not found"**
- Check your .env file exists
- Make sure ANTHROPIC_API_KEY is set
- No quotes needed around the value

**Error: "Database connection failed"**
```bash
# Use SQLite for quick start (no setup needed)
# In .env, set:
DATABASE_URL=sqlite:///./noni.db
```

### Frontend won't start

**Error: "Cannot find module"**
```bash
npm install
```

**Error: "Port 3000 already in use"**
```bash
# Kill the process or use different port
npm run dev -- -p 3001
```

### Voice not working

- Use Chrome or Safari (best support)
- Click "Allow" when asked for microphone access
- Check browser console (F12) for errors
- Try chat interface instead (always works)

### AI not responding

**Check backend is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

**Check API key:**
```bash
cd backend
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key:', os.getenv('ANTHROPIC_API_KEY')[:10])"
# Should print first 10 chars of your key
```

---

## 📁 What You Have Now

```
noni/
├── backend/          # ✅ Running on :8000
│   └── venv/        # ✅ Python dependencies installed
├── frontend/         # ✅ Running on :3000
│   └── node_modules/ # ✅ Node dependencies installed
└── README.md
```

---

## 🎯 Next Steps

### Today
- [x] Get API key
- [x] Start backend
- [x] Start frontend
- [x] Test voice & chat
- [ ] Add a test medication
- [ ] Customize the AI prompt

### Tomorrow
- [ ] Set up proper PostgreSQL database
- [ ] Start Google Calendar integration
- [ ] Deploy to Vercel (frontend)

### This Week
- [ ] Set up Plaid for banking
- [ ] Add your mother's medications
- [ ] Configure caregiver contact
- [ ] Test with family

---

## 🔄 Daily Development Workflow

### Starting your dev environment:

**Terminal 1 (Backend):**
```bash
cd /users/adamjones/noni/backend
source venv/bin/activate
python app/main.py
```

**Terminal 2 (Frontend):**
```bash
cd /users/adamjones/noni/frontend
npm run dev
```

### Stopping:
- Press `Ctrl+C` in both terminals

---

## 💡 Quick Tips

### Adding a test medication:

```bash
curl -X POST http://localhost:8000/api/medications \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin",
    "dosage": "81mg",
    "frequency": "daily",
    "times": ["08:00", "20:00"],
    "user_id": 1
  }'
```

### Testing the AI:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What pills should I take?",
    "user_id": 1,
    "conversation_history": []
  }'
```

### Viewing API docs:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

---

## 🎨 Customizing the AI

Edit `backend/app/services/ai_service.py`:

```python
# Change the system prompt to customize personality
self.system_prompt = """You are a caring AI assistant..."""
```

The AI is designed to be:
- Patient with repetition
- Simple, clear language
- Warm and friendly
- Safety-focused

---

## 📚 Learning Resources

**FastAPI (Backend):**
- https://fastapi.tiangolo.com/

**Next.js (Frontend):**
- https://nextjs.org/docs

**Anthropic Claude:**
- https://docs.anthropic.com/

**PostgreSQL:**
- https://www.postgresql.org/docs/

---

## 🆘 Getting Help

**Check logs:**
- Backend: Look at terminal where `python app/main.py` is running
- Frontend: Check browser DevTools (F12) → Console

**Common issues:**
1. Port already in use → Change port or kill process
2. Module not found → Reinstall dependencies
3. API key invalid → Check .env file
4. Database errors → Switch to SQLite temporarily

**Still stuck?**
- Check the main README.md
- Review API_SETUP_GUIDE.md
- Ask Claude Code or Cursor for specific errors

---

## ✨ You're Ready!

You now have a working AI-native care companion running locally.

**Try these commands:**
- "What time is it?"
- "Hello, how are you?"
- "What can you help me with?"
- "What's on my calendar?" (will say integration pending)

The AI is designed specifically for your mother's needs - patient, clear, and caring.

**Next:** Set up integrations and start testing!
