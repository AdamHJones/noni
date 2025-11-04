# Care Companion - MVP

AI-native care companion for helping your mother with Alzheimer's and dementia manage daily tasks with dignity and independence.

## 🎯 What This MVP Includes

**Core Features:**
- ✅ Voice & Chat interface with Claude AI
- ✅ Patient, empathetic AI responses designed for Alzheimer's care
- ✅ Medication tracking and reminders
- ✅ Basic safety features and emergency detection
- 🔄 Calendar integration (ready to connect)
- 🔄 Banking integration (ready to connect)

**Tech Stack:**
- **Backend:** Python + FastAPI (AI-native, async)
- **Frontend:** Next.js 14 + TypeScript + Tailwind
- **AI:** Claude Sonnet 4.5 (Anthropic)
- **Database:** PostgreSQL (via Supabase recommended)
- **Deployment:** Vercel (frontend) + Railway/DO (backend)

## 📁 Project Structure

```
noni/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── core/        # Config, database
│   │   ├── services/    # AI, Calendar, Banking services
│   │   ├── models/      # Database models
│   │   ├── routes/      # API routes (in main.py for now)
│   │   └── main.py      # FastAPI app
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # Pages (App Router)
│   │   ├── components/ # React components
│   │   └── lib/        # API client, utils
│   ├── package.json
│   └── .env.local.example
│
├── docs/               # Additional documentation
└── pre-read/          # Your original planning docs
```

## 🚀 Quick Start (15 minutes)

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (or Supabase account)
- Anthropic API key

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your API keys (see API_SETUP_GUIDE.md)

# Create database (if using local PostgreSQL)
# Or use Supabase connection string

# Run the server
python app/main.py
# Server runs on http://localhost:8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.local.example .env.local
# Edit .env.local if needed

# Run development server
npm run dev
# Frontend runs on http://localhost:3000
```

### 3. Open in Browser

Visit http://localhost:3000 and you'll see:
- Voice interface (tap to speak)
- Chat interface (type messages)
- Quick action buttons

## 📖 Next Steps

### Immediate (Today)
1. **Get Anthropic API Key** - See `docs/API_SETUP_GUIDE.md`
2. **Test the voice interface** - Works in Chrome/Safari
3. **Add a test medication** - Use the API or database directly

### This Week
1. **Set up Google Calendar API** - See setup guide
2. **Set up Plaid (banking)** - Start with sandbox mode
3. **Add your mother's medications** to the database
4. **Configure caregiver contact info**

### This Month
1. **Deploy to production** (Vercel + Railway)
2. **Test with your mother** (supervised sessions)
3. **Iterate based on feedback**
4. **Add more integrations** as needed

## 🔑 API Keys You'll Need

**Required for MVP:**
- ✅ Anthropic API Key (Claude) - **Required to start**

**Optional (add later):**
- Google Cloud (Calendar, Gmail) - Free tier available
- Plaid (Banking) - Sandbox is free
- Twilio (SMS) - $20/month
- OpenAI (Whisper voice) - Optional, browser voice works

See `docs/API_SETUP_GUIDE.md` for detailed instructions.

## 💾 Database Setup

**Option 1: Supabase (Recommended for MVP)**
```bash
# 1. Sign up at supabase.com
# 2. Create new project
# 3. Copy connection string to .env as DATABASE_URL
# 4. Tables will auto-create on first run
```

**Option 2: Local PostgreSQL**
```bash
# Install PostgreSQL
# Create database
createdb noni_db

# Add to .env
DATABASE_URL=postgresql://user:password@localhost:5432/noni_db
```

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test  # (tests coming soon)
```

## 📱 Using the App

### Voice Interface
1. Click the microphone button
2. Allow browser access to microphone
3. Speak naturally: "What's on my calendar today?"
4. AI responds with voice + text

### Chat Interface
1. Click "Type" tab
2. Type your message
3. AI responds (and speaks the response)

### Quick Actions
- Pre-configured questions
- One tap to ask common questions
- Coming soon: Calendar, Balance, Pills, Messages

## 🔒 Security Notes

**Current State (MVP):**
- API keys in .env files (not committed to git)
- No authentication yet (single user)
- Read-only banking (Plaid)
- Approved contacts whitelist

**Before Production:**
- [ ] Add proper authentication
- [ ] Encrypt sensitive tokens in database
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Set up monitoring

## 🐛 Troubleshooting

**"Module not found" errors:**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

**Database connection errors:**
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Tables will auto-create

**API errors:**
- Check ANTHROPIC_API_KEY in .env
- Verify API key is valid
- Check backend logs

**Voice not working:**
- Use Chrome or Safari (best support)
- Allow microphone access
- Check browser console for errors

## 📚 Documentation

- `docs/API_SETUP_GUIDE.md` - How to get all API keys
- `docs/DEPLOYMENT_GUIDE.md` - Deploy to production
- `docs/DEVELOPMENT_GUIDE.md` - Development best practices
- `pre-read/` - Your original planning documents

## 🤝 Development with AI Tools

This project is designed to work seamlessly with:
- **Claude Code** - For backend Python development
- **Cursor** - For frontend React/TypeScript
- **Codex** - For general coding assistance

All services are in separate files for easy AI-assisted development.

## 💰 Costs (MVP)

**Development:** Free (your time)

**Monthly Operating:**
- Anthropic Claude API: ~$10-20/month (moderate use)
- Supabase: Free tier (upgrade at $25/month if needed)
- Vercel: Free tier
- Railway/DO: $5-10/month
- **Total: $15-30/month to start**

## 🎯 Roadmap

**v0.1 (Current MVP):**
- [x] Voice & chat interface
- [x] AI orchestration with Claude
- [x] Medication tracking
- [ ] Calendar integration
- [ ] Banking integration

**v0.2 (Next 2 weeks):**
- [ ] Google Calendar API connected
- [ ] Plaid banking connected
- [ ] Caregiver dashboard (basic)
- [ ] Emergency contact system

**v0.3 (Month 2):**
- [ ] SMS/messaging integration
- [ ] Photo recognition for people
- [ ] Medication adherence tracking
- [ ] Better error handling

**v1.0 (Production):**
- [ ] Full authentication
- [ ] Multi-user support
- [ ] Advanced security
- [ ] Analytics dashboard
- [ ] Mobile app versions

## ❤️ Philosophy

This application is built with deep respect for your mother's dignity and independence. The AI is:
- **Patient** - Never frustrated by repetition
- **Clear** - Simple language, short sentences
- **Empowering** - Helps, doesn't control
- **Safe** - Multiple confirmation layers
- **Caring** - Warm, friendly tone

## 📞 Support

If you get stuck:
1. Check the troubleshooting section above
2. Review the API setup guide
3. Check backend logs: Look at terminal output
4. Check frontend console: Open browser DevTools
5. Ask Claude Code or Cursor for help with specific errors

## 🚀 Let's Build This!

You have everything you need to start. The hardest part is done - the architecture and core code are ready.

**Start here:**
1. Get your Anthropic API key (5 minutes)
2. Start the backend (2 minutes)
3. Start the frontend (2 minutes)
4. Test the voice interface (1 minute)

Let me know what you need help with next!
