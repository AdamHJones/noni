# Care Companion - AI Agent Architecture
## Application for Alzheimer's Patient Technology Management

**Last Updated:** October 29, 2025  
**Purpose:** Simplified, safe, voice-first interface for managing daily technology needs

---

## 1. SYSTEM ARCHITECTURE OVERVIEW

### Core Design Philosophy
- **Voice-First:** Primary interaction through natural speech
- **Safety-First:** Multiple confirmation layers for actions
- **Dignity-Preserving:** Patient, non-condescending responses
- **Caregiver-Connected:** Transparent oversight without feeling monitored
- **Forgiveness-Built-In:** Handles repetition and confusion gracefully

### Technology Stack Recommendation

#### Frontend Layer
- **Mobile App:** React Native (iOS/Android)
- **Voice Interface:** Whisper API (OpenAI) for speech-to-text
- **Text-to-Speech:** ElevenLabs or Azure TTS (natural, warm voice)
- **UI Framework:** Large buttons, high contrast (WCAG AAA compliance)
- **Offline Capability:** Core functions work without internet

#### Backend Layer
- **AI Orchestration:** Claude API (Anthropic) - patient, contextual responses
- **Application Server:** Node.js/Express or Python/FastAPI
- **Database:** PostgreSQL (interaction history, preferences, contacts)
- **Cache Layer:** Redis (frequent requests, session management)
- **Message Queue:** RabbitMQ or AWS SQS (async notifications)

#### Integration Layer
- **Calendar:** Google Calendar API, Apple Calendar
- **Email:** Gmail API, Microsoft Graph API
- **Banking:** Plaid API (read-only financial aggregation)
- **Healthcare:** FHIR API for medical records (where available)
- **SMS/Messaging:** Twilio API
- **Emergency:** Direct integration with emergency contacts

#### Security & Privacy Layer
- **Authentication:** Biometric (Face ID/fingerprint) + simple PIN backup
- **Authorization:** Role-based (Patient/Caregiver/Healthcare Provider)
- **Encryption:** AES-256 at rest, TLS 1.3 in transit
- **Audit Logging:** Complete activity trail for compliance
- **HIPAA Compliance:** Business Associate Agreements where applicable

---

## 2. FUNCTIONAL ARCHITECTURE

### Module 1: Voice Interaction Engine

**Capabilities:**
- Continuous listening mode (opt-in)
- Wake word: "Hello Helper" or custom name
- Context-aware responses (remembers conversation)
- Patience handling (long pauses, repeated questions)
- Clarification without frustration

**Technical Flow:**
```
User speaks → Whisper STT → Intent Recognition (Claude) → 
Action Router → Execute/Confirm → TTS Response → User hears
```

**Special Handling:**
- Repeated questions: "As I mentioned before..." (gentle reminder)
- Confusion: Simplifies explanation automatically
- Forgetting context: Reintroduces information naturally
- Emotional distress: Recognizes keywords, offers comfort/contacts caregiver

### Module 2: Information Dashboard (Read-Only)

**Finance View:**
- Account balances (updated daily)
- Recent transactions (last 7 days)
- Upcoming bills with amounts
- "Do I have enough money?" → Simple yes/no + amount
- NO account numbers shown (security)

**Calendar View:**
- Today's schedule (large cards)
- "What am I doing today?" voice query
- Upcoming week at a glance
- Medication reminders integrated
- Doctor appointments highlighted

**Communication View:**
- Recent messages (last 3 days)
- Unread count by person
- "Do I have any messages?" → Summary
- Photo + name for each contact (memory aid)
- Voice reads messages aloud

**Healthcare Dashboard:**
- Today's medications (with images)
- "What pills should I take?" → Show + read
- Recent doctor visits summary
- Upcoming appointments
- Emergency contacts (one-tap call)

### Module 3: Safe Action Engine

**Action Categories:**

**GREEN (Always Allowed):**
- View any information
- Listen to messages/emails
- Check calendar
- See weather, time, date
- Call emergency contacts
- Play music/podcasts
- Set simple reminders

**YELLOW (Confirmation Required):**
- Send text message (shows preview, "Send this?")
- Reply to email (reads draft, confirms)
- Add calendar event (confirms details)
- Call non-emergency contacts (confirms who)

**RED (Caregiver Approval Required):**
- Pay bills over $X threshold
- Send money to anyone
- Schedule appointments
- Purchase anything
- Share location
- Add new contacts

**Implementation:**
```
Action Request → Risk Assessment → 
  If GREEN: Execute
  If YELLOW: Confirm with user → Execute
  If RED: Queue for approval → Notify caregiver → Execute after approval
```

### Module 4: Memory Support System

**Interaction History:**
- Stores all conversations (searchable by caregiver)
- "What did I do yesterday?" → Activity summary
- "Who called me this week?" → List with dates
- "When is my next appointment?" → Calendar search

**People Recognition:**
- Photo database of family/friends
- "Who is this?" + photo → Name + relationship
- "When did I last see [name]?" → Date + activity
- Proactive reminders: "Sarah visits on Thursdays"

**Routine Tracking:**
- Learns daily patterns
- Medication adherence monitoring
- Unusual behavior detection (alerts caregiver)
- "Did I take my medicine?" → Check + confirm

### Module 5: Caregiver Dashboard

**Real-Time Monitoring:**
- Live activity feed (non-intrusive)
- Unusual request alerts
- Medication compliance tracking
- Communication summary

**Approval Queue:**
- RED actions waiting for approval
- One-click approve/deny with context
- Can set auto-approve rules

**Health Insights:**
- Conversation patterns (declining cognition indicators)
- Activity level tracking
- Sleep pattern changes (if device worn)
- Confusion frequency metrics

**Configuration:**
- Adjust approval thresholds
- Add/remove trusted contacts
- Update medication schedules
- Set quiet hours

---

## 3. INTEGRATION SPECIFICATIONS

### Financial Integration (Plaid API)

**Read-Only Access:**
- Account balances
- Transaction history (30 days)
- Scheduled payments
- Bill due dates

**Security:**
- No ability to transfer money without approval
- Masked account numbers
- Daily update schedule (not real-time for safety)

**Voice Queries Supported:**
- "How much money do I have?"
- "Did my Social Security check arrive?"
- "What bills are due?"
- "Can I afford to buy [item]?"

### Calendar Integration

**Providers:**
- Google Calendar
- Apple Calendar
- Microsoft Outlook

**Features:**
- Read all events
- Create events (with confirmation)
- Delete events (RED - requires approval)
- Recurring reminders for daily routines

**Voice Queries:**
- "What's on my calendar?"
- "Do I have anything tomorrow?"
- "When is my doctor appointment?"
- "Remind me to call John at 3pm"

### Email Integration

**Providers:**
- Gmail API
- Microsoft Graph (Outlook)

**Safety Features:**
- Read-only by default
- Reply only to known contacts
- No attachments sent without approval
- Spam filtered at API level

**Voice Queries:**
- "Do I have any emails?"
- "Read my emails from [name]"
- "Reply to [name]: [message]" → Confirms before sending
- "Delete spam" (safe, bulk action)

### SMS/Text Integration (Twilio)

**Features:**
- Receive all texts
- Send to approved contacts only
- Cannot add new contacts without caregiver
- Read aloud on request

**Voice Queries:**
- "Do I have any texts?"
- "Read texts from Sarah"
- "Text Sarah: I love you" → Confirms recipient + message
- "Who texted me today?"

### Healthcare Integration

**Medical Records (FHIR API where available):**
- Medication list
- Allergy information
- Recent test results (simplified)
- Immunization records

**Medication Management:**
- Visual + audio reminders
- "Show me my pills" → Photos of actual medications
- Adherence tracking
- Refill reminders (notifies caregiver)

**Doctor Portal Integration:**
- Appointment scheduling (read-only)
- Recent visit summaries
- Upcoming appointments
- Provider contact info

---

## 4. USER EXPERIENCE DESIGN

### Voice Interaction Examples

**Good Morning Routine:**
```
App: "Good morning! It's Wednesday, October 30th. 
      You have two things today: 
      Doctor appointment at 2pm, and 
      Sarah is visiting at 4pm. 
      Would you like to hear your messages?"
```

**Financial Query:**
```
User: "Do I have enough money?"
App: "Yes, you have $3,847 in your checking account. 
      Your bills are all paid this month. 
      You're doing great!"
```

**Confused Repetition:**
```
User: "When is my appointment?" (3rd time asking)
App: "Your doctor appointment is at 2pm today. 
      That's in about 4 hours. 
      I'll remind you an hour before. 
      Would you like me to write it down for you?"
```

**Action Confirmation:**
```
User: "Text Sarah I miss her"
App: "I'll send this text to Sarah your daughter: 
      'I miss her' 
      Should I send this?"
User: "Yes"
App: "Sent! Sarah will get it right away."
```

### Visual Design Guidelines

**Colors:**
- High contrast (black text on white, or white on dark blue)
- Color-blind friendly palette
- No red/green for critical info

**Typography:**
- Minimum 18pt font (adjustable to 24pt)
- Sans-serif (Arial, Roboto)
- 1.5x line spacing
- Left-aligned (easier to read)

**Layout:**
- One primary action per screen
- Huge buttons (minimum 60px height)
- 3-4 items maximum per list
- Lots of white space

**Icons:**
- Simple, universally recognized
- Always paired with text labels
- High contrast outlines

---

## 5. SAFETY & ERROR HANDLING

### Confusion Detection

**Indicators:**
- Repeated identical questions (>3 times/hour)
- Contradictory statements
- Time disorientation
- Person recognition failures
- Aggressive/unusual language

**Response:**
- Gentle redirection
- Simplified explanations
- Notify caregiver if severe
- Offer to call someone
- De-escalation phrases built-in

### Emergency Handling

**Trigger Words:**
- "Help", "Emergency", "Hurt", "Fell", "Can't breathe"
- "Lost", "Scared", "Don't know where I am"

**Automatic Actions:**
1. Ask "Are you okay? Should I call for help?"
2. If yes or no response: Call emergency contact
3. If still no response (30 sec): Call 911
4. Send location to emergency contacts
5. Keep line open, provide comfort

### Privacy Safeguards

**What's Never Recorded:**
- Financial account numbers
- Social Security numbers
- Passwords or PINs
- Medical record numbers

**What's Encrypted End-to-End:**
- All voice recordings
- Message content
- Location data
- Health information

**Retention Policies:**
- Voice recordings: 30 days then deleted
- Transcripts: 90 days for pattern analysis
- Activity logs: 1 year for healthcare needs
- Analytics only: Anonymous, aggregated

---

## 6. DEPLOYMENT ARCHITECTURE

### Infrastructure

**Production Environment:**
- Cloud: AWS or Azure (HIPAA compliant regions)
- Container orchestration: Kubernetes
- Load balancing: ALB/Azure Load Balancer
- CDN: CloudFront for static assets
- Monitoring: DataDog or New Relic

**Database Setup:**
- Primary: PostgreSQL RDS (Multi-AZ)
- Replica: Read replica for analytics
- Backup: Daily automated, 30-day retention
- Encryption: At rest with KMS

**API Gateway:**
- Rate limiting (prevent abuse)
- Authentication layer
- Request logging
- DDoS protection

### Scalability

**Current Design Supports:**
- Single user (your mother) optimized
- Extensible to family members
- Could scale to 100k+ users with current architecture

**Performance Targets:**
- Voice response: <2 seconds
- UI interactions: <500ms
- Calendar/email sync: Every 15 minutes
- Financial data: Daily refresh

---

## 7. DEVELOPMENT ROADMAP

### Phase 1: MVP (4-6 weeks)
- Voice interface basics
- Calendar view (read-only)
- Simple reminders
- Emergency contacts
- Caregiver dashboard (basic)

### Phase 2: Core Features (6-8 weeks)
- Email integration (read + reply)
- SMS integration
- Financial dashboard (Plaid)
- Medication reminders
- People recognition

### Phase 3: Advanced (8-10 weeks)
- Healthcare records integration
- Advanced memory support
- Pattern recognition (cognition tracking)
- Multi-user support
- Enhanced security features

### Phase 4: Polish (4-6 weeks)
- Accessibility improvements
- Performance optimization
- Extended testing with users
- Documentation
- Training materials

**Total Timeline: 22-30 weeks (5.5-7.5 months)**

---

## 8. COST ESTIMATION

### Development Costs (One-Time)
- Senior Full-Stack Developer: $120k-150k (6 months)
- AI/ML Engineer: $80k-100k (3 months)
- UI/UX Designer (Accessibility): $40k-50k (2 months)
- QA/Testing: $30k-40k (ongoing)
- Project Management: $20k-30k
- **Total Development: $290k-370k**

### Operational Costs (Monthly per user)
- Cloud Infrastructure: $50-100
- Claude API: $20-40 (moderate use)
- Plaid API: $5
- Twilio (SMS): $10-20
- Other APIs: $10-20
- **Total Monthly: $95-185 per user**

### Alternatives for Lower Cost
- Self-host voice models (Whisper): Saves $15/mo
- Use cheaper LLM for basic queries: Saves $10-20/mo
- Annual API subscriptions: Save 15-20%
- **Optimized Monthly: $60-120 per user**

---

## 9. REGULATORY COMPLIANCE

### HIPAA (Healthcare)
- Business Associate Agreements with all vendors
- Encrypted PHI storage and transmission
- Access logging and monitoring
- Breach notification procedures
- Regular security audits

### ADA (Accessibility)
- WCAG 2.1 Level AAA compliance
- Screen reader compatible
- Voice-only operation possible
- High contrast modes
- Adjustable text sizing

### Data Protection
- GDPR compliant (if expanding internationally)
- Right to deletion
- Data portability
- Consent management
- Privacy policy in simple language

### Financial
- No PCI compliance needed (read-only)
- SOC 2 Type II for data handling
- Plaid handles all financial security

---

## 10. SUCCESS METRICS

### User Engagement
- Daily active usage
- Voice interactions per day
- Successfully completed tasks
- User satisfaction (via caregiver)

### Safety Metrics
- False emergency alerts (target: <1/month)
- Successful confirmations (target: >95%)
- Caregiver approval response time
- Zero unauthorized financial transactions

### Health Outcomes
- Medication adherence rate (target: >90%)
- Appointment attendance
- Social interaction frequency
- Reduced caregiver anxiety (survey-based)

### Technical Performance
- System uptime (target: 99.9%)
- Voice recognition accuracy (target: >95%)
- Response time (target: <2 seconds)
- Error rate (target: <1%)

---

## APPENDIX A: Alternative Architectures

### Simpler Approach (Faster, Lower Cost)
- Use existing platforms: Alexa Skills + IFTTT
- Pre-built voice assistant customization
- Less custom development
- Trade-off: Less control, less tailored experience
- **Cost: $20k-40k development, $20-30/mo operations**

### Enterprise Approach (Hospital/Care Facility Scale)
- Multi-tenant architecture
- Healthcare provider integrations (Epic, Cerner)
- Advanced analytics dashboard
- Regulatory compliance team
- **Cost: $1M-2M development, economies of scale**

---

## APPENDIX B: Technology Alternatives

### Voice Recognition
- **Whisper (OpenAI):** Most accurate, $0.006/min
- **Google Speech-to-Text:** Good, $0.024/min
- **Azure Speech:** HIPAA compliant, $0.024/min
- **Amazon Transcribe:** AWS ecosystem, $0.024/min

### AI/LLM
- **Claude (Anthropic):** Best for empathetic, patient responses
- **GPT-4 (OpenAI):** Excellent, slightly more expensive
- **Gemini (Google):** Multimodal strength
- **Local models (Llama):** Privacy, higher infrastructure cost

### Text-to-Speech
- **ElevenLabs:** Most natural, emotional
- **Azure Neural TTS:** HIPAA compliant
- **Google Cloud TTS:** Good quality, affordable
- **Amazon Polly:** Reliable, AWS ecosystem

---

## NEXT STEPS

1. **Review this architecture** with stakeholders
2. **Get healthcare provider input** (her doctor)
3. **Pilot with your mother** (consent + testing)
4. **Select development team** (or I can help build prototype)
5. **Secure funding** if scaling beyond personal use
6. **Begin Phase 1 development**

This is a challenging but deeply meaningful project. I'm here to help you build it.
