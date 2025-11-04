# UI/UX Specifications - Three-Tier User Experience

## Design Philosophy by Role

### Patient: "Grandma-Proof" Simplicity
**Motto**: "If my grandmother with Alzheimer's can't use it in 3 seconds, it's too complex"

### Caregiver: "Efficient Task Management"
**Motto**: "Capture everything important while caring, without breaking flow"

### Family/Admin: "Complete Visibility & Control"
**Motto**: "See everything, control everything, understand everything"

---

## PATIENT INTERFACE

### Design Principles

1. **Voice-First, Always**
   - Big microphone button (center, always visible)
   - Visual feedback (pulsing, color change)
   - Immediate voice response

2. **Maximum Simplicity**
   - One primary action per screen
   - No hidden menus or hamburger icons
   - No scrolling when possible
   - No forms or text input (voice only)

3. **Forgiving & Patient**
   - No error messages that blame user
   - Infinite retries
   - AI explains what went wrong simply
   - No timeouts or forced actions

4. **Visual Clarity**
   - 24pt minimum font size (adjustable to 36pt)
   - High contrast (WCAG AAA)
   - Large buttons (minimum 80px height)
   - Generous whitespace
   - Photos over text (show their caregiver's face, not just name)

5. **Familiar Patterns**
   - Green = safe/good
   - Red = important/stop
   - Yellow = warning/wait
   - Blue = information

---

### Screen Layouts

#### Screen 1: HOME (Default)

```
┌─────────────────────────────────────┐
│  🤗 Hi Dorothy!                      │
│  Thursday, January 15 • 10:30 AM   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│                                     │
│          [🎤 MICROPHONE]            │
│         (144px × 144px)             │
│                                     │
│    "Tap and ask me anything"       │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  👤 Your Caregiver Today:           │
│                                     │
│  [PHOTO: Sarah]                     │
│  Sarah Johnson                      │
│  ⭐⭐⭐⭐⭐                           │
│  Arrives at 3:00 PM                 │
│                                     │
│  [Call Sarah]  [When is she coming?]│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Quick Help:                        │
│                                     │
│  [📅 What's today?]                 │
│  [💊 My pills]                      │
│  [💬 My messages]                   │
│  [📞 Call family]                   │
└─────────────────────────────────────┘

[Bottom Bar]
🏠 Home  |  🗣️ Chat  |  📸 Camera
```

**Interactions**:
- Tap microphone → starts listening (no confirmation)
- Tap quick buttons → AI reads answer aloud + shows on screen
- All buttons are full-width, 80px tall
- No navigation required (everything on home screen)

---

#### Screen 2: CHAT (AI Conversation)

```
┌─────────────────────────────────────┐
│  🤗 Talking with Care Companion      │
│                                     │
│  [🎤] Listening... / Ready          │
└─────────────────────────────────────┘

[Chat Bubbles - Large Text]

┌─────────────────────────────────────┐
│  You:                               │
│  What pills do I take?              │
│  10:32 AM                           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Care Companion:                    │
│                                     │
│  You take 2 pills with breakfast:  │
│                                     │
│  [PHOTO: white pill]                │
│  • Small white pill                 │
│    (blood pressure)                 │
│                                     │
│  [PHOTO: yellow pill]               │
│  • Yellow pill                      │
│    (vitamin D)                      │
│                                     │
│  Would you like me to remind you   │
│  when to take them?                 │
│                                     │
│  10:32 AM                           │
└─────────────────────────────────────┘

[Bottom]
┌─────────────────────────────────────┐
│  [🎤 Ask something else]            │
│  (Auto-playing voice response...)   │
└─────────────────────────────────────┘

[Bottom Bar]
🏠 Home  |  🗣️ Chat  |  📸 Camera
```

**Key Features**:
- Chat history visible (last 5 messages)
- AI responses include photos when relevant
- Voice auto-plays for AI responses
- Can tap to replay voice
- Simple "Ask something else" button (no text input)

---

#### Screen 3: CAMERA (Photo Analysis)

```
┌─────────────────────────────────────┐
│  📸 Take a Photo                    │
│                                     │
│  I can help you read:               │
└─────────────────────────────────────┘

[Large Icon Buttons - 2 columns]

┌──────────────────┬──────────────────┐
│  💊 Prescription │  🏷️ Medicine    │
│                  │     Bottle       │
│  [Take Photo]    │  [Take Photo]    │
└──────────────────┴──────────────────┘

┌──────────────────┬──────────────────┐
│  📋 Doctor Note  │  🍳 Recipe       │
│                  │                  │
│  [Take Photo]    │  [Take Photo]    │
└──────────────────┴──────────────────┘

┌──────────────────┬──────────────────┐
│  🥫 Food Label   │  📊 Nutrition    │
│                  │                  │
│  [Take Photo]    │  [Take Photo]    │
└──────────────────┴──────────────────┘

┌─────────────────────────────────────┐
│  🔤 Small Text / Sign                │
│                                     │
│  [Take Photo]                       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Or ask me what to photograph:      │
│  [🎤 "What should I scan?"]         │
└─────────────────────────────────────┘

[Bottom Bar]
🏠 Home  |  🗣️ Chat  |  📸 Camera
```

**After Taking Photo**:

```
┌─────────────────────────────────────┐
│  [Photo preview]                    │
│  (tap to retake)                    │
└─────────────────────────────────────┘

[Loading Animation]
🔄 Reading your photo...

[Then Shows Results in Large Text]

┌─────────────────────────────────────┐
│  ✅ This is safe!                   │
│                                     │
│  This is: Aspirin 81mg              │
│  What it's for: Heart health        │
│  When to take: Once daily (evening) │
│                                     │
│  ✓ You already take this medicine   │
│  ✓ No problems found                │
│                                     │
│  [🔊 Read to me again]              │
│  [✓ Got it]                         │
└─────────────────────────────────────┘
```

---

#### Screen 4: MY MESSAGES

```
┌─────────────────────────────────────┐
│  💬 Your Messages                   │
└─────────────────────────────────────┘

[Message Cards - Large]

┌─────────────────────────────────────┐
│  [PHOTO: Sarah]                     │
│  From: Sarah (Your Daughter)        │
│  Today at 9:15 AM                   │
│                                     │
│  "Hi Mom! I'll visit tomorrow       │
│   at noon. Love you!"               │
│                                     │
│  [🔊 Read to me]  [❤️ Reply "Love  │
│                        you too"]    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  [PHOTO: Michael]                   │
│  From: Michael (Your Son)           │
│  Yesterday at 3:42 PM               │
│                                     │
│  "How are you feeling today?"      │
│                                     │
│  [🔊 Read to me]  [Reply]           │
└─────────────────────────────────────┘

[Bottom]
┌─────────────────────────────────────┐
│  [🎤 Send a message]                │
└─────────────────────────────────────┘

[Bottom Bar]
🏠 Home  |  🗣️ Chat  |  📸 Camera
```

**Reply Flow** (if patient taps Reply):

```
[Voice activates]
"What would you like to say to Sarah?"

[Patient speaks]
Patient: "I love you too, see you tomorrow"

[Shows confirmation]
┌─────────────────────────────────────┐
│  Send this message to Sarah?        │
│                                     │
│  "I love you too,                   │
│   see you tomorrow"                 │
│                                     │
│  [✓ Yes, send it]  [✗ No, cancel]  │
└─────────────────────────────────────┘
```

---

### Patient UI Component Library

#### Buttons

```css
/* Primary Action Button (Voice, Call, etc.) */
.patient-btn-primary {
  min-height: 80px;
  font-size: 24px;
  border-radius: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 700;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
  padding: 20px 40px;
  width: 100%;
  margin: 10px 0;
}

/* Secondary Action Button */
.patient-btn-secondary {
  min-height: 70px;
  font-size: 20px;
  border-radius: 15px;
  background: white;
  border: 3px solid #667eea;
  color: #667eea;
  font-weight: 600;
  padding: 15px 30px;
  width: 100%;
  margin: 10px 0;
}

/* Quick Action Tile */
.patient-quick-action {
  min-height: 120px;
  font-size: 20px;
  border-radius: 20px;
  background: #f8f9ff;
  border: 2px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  gap: 10px;
}

.patient-quick-action-icon {
  font-size: 48px;
}
```

#### Text Styles

```css
.patient-heading {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.3;
}

.patient-body {
  font-size: 24px;
  font-weight: 400;
  color: #374151;
  line-height: 1.6;
}

.patient-label {
  font-size: 18px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

#### Color Palette

```css
/* Patient Interface Colors */
:root {
  --patient-primary: #667eea;
  --patient-secondary: #764ba2;
  --patient-success: #4ade80;
  --patient-warning: #fbbf24;
  --patient-danger: #f87171;
  --patient-background: #ffffff;
  --patient-surface: #f8f9ff;
  --patient-text: #1f2937;
  --patient-text-light: #6b7280;
}
```

---

## CAREGIVER INTERFACE

### Design Principles

1. **Task-Oriented**
   - Checklists and completion tracking
   - Clear "what's next" guidance
   - Quick capture (photo, note, log)

2. **Mobile-Optimized**
   - One-handed operation when possible
   - Offline-capable (sync later)
   - Quick toggles and swipes

3. **Time-Aware**
   - Clock in/out prominent
   - Time tracking visible
   - Schedule at-a-glance

4. **Evidence-Based**
   - Easy photo capture for everything
   - Automatic timestamps
   - Activity logging built into workflow

5. **Professional**
   - Clean, modern design
   - Business-appropriate colors
   - Data-dense but organized

---

### Screen Layouts

#### Screen 1: TODAY'S SCHEDULE (Home)

```
┌─────────────────────────────────────┐
│  Care Companion · Caregiver         │
│  Thursday, January 15               │
│                                     │
│  Sarah K. ⭐ 4.9                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  📊 Today's Overview                │
│                                     │
│  3 sessions · 11 hours · $275      │
│  [View Week] [Availability]         │
└─────────────────────────────────────┘

[Patient Session Cards]

┌─────────────────────────────────────┐
│  🟢 IN PROGRESS                     │
│                                     │
│  👤 Dorothy M. (78)                 │
│  📍 2.3 miles · 123 Oak St          │
│  ⏱️ 9:00 AM - 12:00 PM (3 hrs)      │
│  💰 $25/hr = $75                    │
│                                     │
│  Started: 9:03 AM (2h 15m ago)     │
│                                     │
│  Tasks: 3/6 completed ✓             │
│  ☑ Arrived & greeted               │
│  ☑ Morning meds (photo logged)     │
│  ☑ Breakfast prepared              │
│  ☐ Walk together                   │
│  ☐ Lunch preparation               │
│  ☐ End session notes               │
│                                     │
│  [📸 Quick Photo] [📝 Add Note]    │
│  [✓ End Session]                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  ⏰ UPCOMING                        │
│                                     │
│  👤 Robert K. (81)                  │
│  📍 5.1 miles · 456 Maple Ave       │
│  ⏱️ 3:00 PM - 5:00 PM (2 hrs)       │
│  💰 $25/hr = $50                    │
│                                     │
│  Tasks:                             │
│  • Afternoon meds                   │
│  • Accompany to doctor appt         │
│  • Post-appointment notes           │
│                                     │
│  [🗺️ Navigate] [📋 Care Plan]      │
│  [▶️ Start Session (at 2:45 PM)]   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  ✓ COMPLETED TODAY                  │
│                                     │
│  👤 Margaret P. (76) - 7:00-9:00 AM │
│  ⏱️ 2 hours · $50 earned            │
│  ⭐ [Rate This Session]             │
└─────────────────────────────────────┘

[Bottom Navigation]
📅 Schedule | 💼 Find Work | 💬 Messages | 👤 Profile
```

---

#### Screen 2: ACTIVE SESSION

```
┌─────────────────────────────────────┐
│  🟢 SESSION ACTIVE                  │
│  Dorothy M. · 2h 18m elapsed        │
│  $25/hr · $57.50 so far            │
└─────────────────────────────────────┘

[Care Checklist - Interactive]

┌─────────────────────────────────────┐
│  Care Tasks (Tap to complete)       │
│                                     │
│  ✅ 9:03 AM · Arrived & greeted     │
│  ✅ 9:15 AM · Morning medications   │
│      [VIEW PHOTO]                   │
│                                     │
│  ✅ 9:30 AM · Breakfast prepared    │
│      Oatmeal with berries           │
│      [VIEW PHOTO]                   │
│                                     │
│  🔄 10:45 AM · Walk together        │
│      [Mark Complete] [Skip]         │
│                                     │
│  ⏸️ Lunch preparation               │
│      Scheduled: 11:30 AM            │
│                                     │
│  ⏸️ Session notes                   │
│      Before ending session          │
└─────────────────────────────────────┘

[Quick Actions - Always Visible]

┌─────────────────────────────────────┐
│  [📸 Take Photo]  [📝 Add Note]     │
│  [💊 Log Med]     [🚨 Report Issue] │
└─────────────────────────────────────┘

[Patient Info - Collapsible]

┌─────────────────────────────────────┐
│  📋 Today's Care Plan               │
│  ▼ Tap to expand                    │
│                                     │
│  Medications:                       │
│  • Donepezil 10mg (morning) ✓       │
│  • Vitamin D 2000 IU (morning) ✓    │
│                                     │
│  Dietary:                           │
│  ⚠️ Dairy allergy                   │
│                                     │
│  Notes from family:                 │
│  "Mom is having trouble sleeping.   │
│   Please note her mood today."      │
│                                     │
│  Emergency: Sarah (daughter)        │
│  [📞 Call]                          │
└─────────────────────────────────────┘

[Location - Small Indicator]

┌─────────────────────────────────────┐
│  📍 At Dorothy's home ✓             │
│  Last updated: 2 min ago            │
└─────────────────────────────────────┘

[End Session]

┌─────────────────────────────────────┐
│  [🛑 End Session & Log Hours]       │
│  (Review tasks first)               │
└─────────────────────────────────────┘

[Bottom Navigation]
📅 Schedule | 💼 Find Work | 💬 Messages | 👤 Profile
```

**End Session Flow**:

```
┌─────────────────────────────────────┐
│  End Session with Dorothy           │
│                                     │
│  Duration: 3h 5m                    │
│  Amount: $77.08                     │
│                                     │
│  Completed tasks: 5/6 ✓             │
│  (Walk together was skipped)        │
│                                     │
│  Session notes (optional):          │
│  ┌───────────────────────────────┐ │
│  │ Dorothy was in great spirits  │ │
│  │ today. She remembered my name │ │
│  │ and talked about her garden.  │ │
│  └───────────────────────────────┘ │
│                                     │
│  [📸 Add final photos] (0 added)   │
│                                     │
│  ☐ Flag any concerns for family     │
│                                     │
│  [✓ Complete Session]               │
│  [Cancel]                           │
└─────────────────────────────────────┘

[After completion]

┌─────────────────────────────────────┐
│  ✅ Session Logged!                 │
│                                     │
│  You'll be paid: $77.08             │
│  (Platform fee: $11.54 deducted)   │
│                                     │
│  Payment processed: Next Friday     │
│                                     │
│  [View Receipt] [Next Appointment]  │
└─────────────────────────────────────┘
```

---

#### Screen 3: PATIENT PROFILE (Caregiver View)

```
┌─────────────────────────────────────┐
│  ← Back to Schedule                 │
│                                     │
│  Dorothy Martinez, 78               │
│  Patient since: Dec 2024            │
│  Your sessions: 24 (72 hours)       │
└─────────────────────────────────────┘

[Tabs]
Care Plan | Medications | History | Contact

---

[Care Plan Tab]

┌─────────────────────────────────────┐
│  📋 Care Plan (Set by Sarah M.)     │
│  Last updated: Jan 10, 2025         │
│                                     │
│  Diagnosis:                         │
│  Early-stage Alzheimer's disease    │
│                                     │
│  Care Level: 2 (Moderate)           │
│  Your certification: Level 3 ✓      │
│                                     │
│  Primary Needs:                     │
│  ✓ Medication reminders (strict)    │
│  ✓ Meal preparation                 │
│  ✓ Light housekeeping               │
│  ✓ Companionship                    │
│  ✗ NO bathing/personal care         │
│                                     │
│  Dietary Restrictions:              │
│  ⚠️ Dairy allergy (severe)          │
│  ⚠️ Low sodium diet                 │
│                                     │
│  Behavioral Notes:                  │
│  • Prefers to be called "Dorothy"   │
│  • Best energy in mornings          │
│  • Enjoys talking about gardening   │
│  • May repeat questions - be patient│
│  • Gentle reminders only            │
│                                     │
│  Emergency Contacts:                │
│  1. Sarah M. (Daughter) - Primary   │
│     📞 [Call] 💬 [Text]             │
│  2. Michael M. (Son) - Secondary    │
│     📞 [Call]                       │
└─────────────────────────────────────┘

---

[Medications Tab]

┌─────────────────────────────────────┐
│  💊 Current Medications (4)         │
│                                     │
│  [PHOTO: white pill]                │
│  Donepezil 10mg                     │
│  • 1x daily (morning with breakfast)│
│  • For: Alzheimer's disease         │
│  • ⚠️ Take with food               │
│                                     │
│  [PHOTO: pink pill]                 │
│  Lisinopril 20mg                    │
│  • 1x daily (morning)               │
│  • For: Blood pressure              │
│                                     │
│  [PHOTO: yellow pill]               │
│  Vitamin D 2000 IU                  │
│  • 1x daily (morning)               │
│  • For: Bone health                 │
│                                     │
│  [PHOTO: white small pill]          │
│  Aspirin 81mg                       │
│  • 1x daily (evening with dinner)   │
│  • For: Heart health                │
│  • ⚠️ Take with food               │
│                                     │
│  [View Adherence History]           │
└─────────────────────────────────────┘

---

[History Tab]

┌─────────────────────────────────────┐
│  📊 Your Sessions with Dorothy      │
│                                     │
│  Last 30 days:                      │
│  • 12 sessions completed            │
│  • 36 hours worked                  │
│  • $900 earned                      │
│  • On-time: 100%                    │
│  • Tasks completed: 98%             │
│                                     │
│  Recent Sessions:                   │
│                                     │
│  Jan 15 · 9:00-12:00 (3h) · $75     │
│  Status: In progress                │
│                                     │
│  Jan 13 · 9:00-12:00 (3h) · $75     │
│  Status: Completed ✓                │
│  Family rating: ⭐⭐⭐⭐⭐           │
│  [View Details]                     │
│                                     │
│  Jan 10 · 9:00-12:00 (3h) · $75     │
│  Status: Completed ✓                │
│  Family rating: ⭐⭐⭐⭐⭐           │
│  [View Details]                     │
│                                     │
│  [View All]                         │
└─────────────────────────────────────┘
```

---

#### Screen 4: FIND WORK (Marketplace)

```
┌─────────────────────────────────────┐
│  💼 Find New Clients                │
│                                     │
│  [Filters] Distance: 10mi | Level: 1-3 | Mon-Fri
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🔔 Recommended for You (3)         │
└─────────────────────────────────────┘

[Care Request Card]

┌─────────────────────────────────────┐
│  ⭐ 96% MATCH · NEW TODAY            │
│                                     │
│  📍 2.1 miles from you              │
│  💰 $28/hour                        │
│                                     │
│  Schedule Needed:                   │
│  Saturdays 10:00 AM - 2:00 PM       │
│  (4 hours/week = $112/week)         │
│                                     │
│  Care Level: 2 (Moderate)           │
│  You: Level 3 ✓                     │
│                                     │
│  Needs:                             │
│  ✓ Medication management            │
│  ✓ Meal preparation                 │
│  ✓ Light housekeeping               │
│  ✓ Dementia support                 │
│  ✓ Own transportation               │
│                                     │
│  Patient (anonymous until matched): │
│  Female, 82, Moderate Alzheimer's   │
│                                     │
│  Family has reviewed 2 applicants   │
│  ⏰ Posted 3 hours ago               │
│                                     │
│  Why great match:                   │
│  • Fits your Saturday availability  │
│  • Your certifications cover all needs
│  • Within your 10-mile preference   │
│  • Rate matches your profile ($25-30)
│                                     │
│  [✓ Apply Now] [View Details]       │
│  [❌ Not Interested]                │
└─────────────────────────────────────┘

[Another Card]

┌─────────────────────────────────────┐
│  ⭐ 88% MATCH                        │
│                                     │
│  📍 7.5 miles · $24/hour            │
│  Mon/Wed 1:00-4:00 PM (6 hrs/wk)    │
│  Level 1 (Basic) - You're qualified │
│                                     │
│  [View Details] [Apply]             │
└─────────────────────────────────────┘

---

┌─────────────────────────────────────┐
│  🔍 All Opportunities (12)          │
│  [Filter] [Sort by: Match]          │
└─────────────────────────────────────┘

[List view of other opportunities...]
```

**Application Flow**:

```
┌─────────────────────────────────────┐
│  Apply for Care Position            │
│                                     │
│  Saturday care · 2.1 miles · $28/hr │
│                                     │
│  Your hourly rate: $28/hr           │
│  (Family budget: $25-30/hr) ✓       │
│                                     │
│  Availability confirmation:         │
│  ☑ I'm available Saturdays 10am-2pm │
│  ☐ I can adjust my schedule if needed
│                                     │
│  Introduction message (optional):   │
│  ┌───────────────────────────────┐ │
│  │ I have 8 years of experience  │ │
│  │ with Alzheimer's patients and │ │
│  │ am certified in dementia care.│ │
│  │ I'd love to meet your family  │ │
│  │ member and discuss their needs│ │
│  └───────────────────────────────┘ │
│                                     │
│  [✓ Submit Application]             │
│  [Cancel]                           │
└─────────────────────────────────────┘

[After submission]

┌─────────────────────────────────────┐
│  ✅ Application Sent!                │
│                                     │
│  The family will review your        │
│  profile and may contact you for    │
│  an interview.                      │
│                                     │
│  Typical response time: 1-2 days    │
│                                     │
│  [🔔 Get notified] [View My Apps]   │
└─────────────────────────────────────┘
```

---

#### Screen 5: EARNINGS & SCHEDULE

```
┌─────────────────────────────────────┐
│  💵 Your Earnings                   │
└─────────────────────────────────────┘

[This Week]

┌─────────────────────────────────────┐
│  Week of Jan 12-18, 2025            │
│                                     │
│  Completed: $450                    │
│  18 hours · 6 sessions              │
│                                     │
│  Scheduled: $300                    │
│  12 hours · 4 sessions remaining    │
│                                     │
│  Total This Week: $750              │
│  (After fees: $637.50)              │
│                                     │
│  [View Breakdown]                   │
└─────────────────────────────────────┘

[Payment Schedule]

┌─────────────────────────────────────┐
│  💰 Next Payout: Friday, Jan 17     │
│                                     │
│  Amount: $637.50                    │
│  (18 hours @ avg $25/hr - 15% fee)  │
│                                     │
│  Direct deposit to: ****6789        │
│  [Update Bank Info]                 │
└─────────────────────────────────────┘

[This Month]

┌─────────────────────────────────────┐
│  January 2025                       │
│                                     │
│  Total Earned: $1,875               │
│  75 hours · 25 sessions             │
│  Avg rate: $25/hour                 │
│                                     │
│  [Download Invoice] [Tax Summary]   │
└─────────────────────────────────────┘

[Weekly Schedule]

┌─────────────────────────────────────┐
│  📅 Your Week                       │
│                                     │
│  Mon Jan 13: 9 hours (3 sessions)   │
│  • Dorothy M. 9am-12pm              │
│  • Robert K. 1pm-3pm                │
│  • Margaret P. 4pm-8pm              │
│                                     │
│  Tue Jan 14: 6 hours (2 sessions)   │
│  Wed Jan 15: 9 hours (3 sessions)   │
│  Thu Jan 16: AVAILABLE              │
│  Fri Jan 17: 6 hours (2 sessions)   │
│  Sat Jan 18: 4 hours (1 session)    │
│  Sun Jan 19: AVAILABLE              │
│                                     │
│  [Update Availability]              │
└─────────────────────────────────────┘
```

---

### Caregiver UI Component Library

```css
/* Caregiver Professional Theme */
:root {
  --caregiver-primary: #0ea5e9; /* Sky blue */
  --caregiver-success: #10b981; /* Green */
  --caregiver-warning: #f59e0b; /* Amber */
  --caregiver-danger: #ef4444; /* Red */
  --caregiver-background: #f8fafc;
  --caregiver-surface: #ffffff;
  --caregiver-text: #0f172a;
  --caregiver-text-light: #64748b;
  --caregiver-border: #e2e8f0;
}

/* Session Status Indicators */
.session-active {
  border-left: 4px solid var(--caregiver-success);
  background: #ecfdf5;
}

.session-upcoming {
  border-left: 4px solid var(--caregiver-primary);
  background: #f0f9ff;
}

.session-completed {
  border-left: 4px solid var(--caregiver-text-light);
  background: #f8fafc;
}

/* Task Checklist */
.task-completed {
  color: var(--caregiver-text-light);
  text-decoration: line-through;
}

.task-current {
  color: var(--caregiver-primary);
  font-weight: 600;
}

.task-pending {
  color: var(--caregiver-text);
}
```

---

## FAMILY/ADMIN INTERFACE

### Design Principles

1. **Data-Rich Dashboards**
   - Multiple widgets and charts
   - Real-time updates
   - Drill-down capabilities
   - Export and reporting

2. **Complete Control**
   - Every setting accessible
   - Clear permission management
   - Audit trails visible
   - Override capabilities

3. **Professional & Trustworthy**
   - Medical-grade interface
   - Clear data visualization
   - Serious tone (this is health data)
   - Confidence-inspiring design

4. **Desktop-First, Mobile-Capable**
   - Multi-column layouts on desktop
   - Responsive for mobile oversight
   - Progressive disclosure (advanced settings hidden by default)

5. **Proactive Insights**
   - Alerts and notifications prominent
   - Trends and patterns highlighted
   - Recommendations from AI
   - Anomaly detection

---

### Screen Layouts

#### Screen 1: FAMILY DASHBOARD (Home)

```
[Desktop Layout - 3 columns]

┌─────────────────────────────────────────────────────────────────┐
│  Care Companion · Family Dashboard                              │
│  Dorothy Martinez                           👤 Sarah (You)      │
│  [Switch Patient ▼] [Settings ⚙️] [Help ?]  [Notifications 🔔3] │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────┬──────────────────┐
│ LEFT COLUMN          │ CENTER COLUMN        │ RIGHT COLUMN     │
│ (Patient Overview)   │ (Activity Feed)      │ (Quick Actions)  │
├──────────────────────┼──────────────────────┼──────────────────┤
│                      │                      │                  │
│ 📊 QUICK STATS       │ 🕐 LIVE ACTIVITY     │ ⚡ QUICK ACTIONS │
│ (Last 7 Days)        │                      │                  │
│                      │ ● Live now           │ [📞 Call Mom]    │
│ Medication:          │ 10:42 AM             │                  │
│ ✅ 96% (67/70)       │ Dorothy asked AI:    │ [💬 Send Msg]    │
│ [View Details]       │ "What's for lunch?"  │                  │
│                      │                      │ [📍 Location]    │
│ Caregiver:           │ 10:15 AM             │ Mom is home ✓    │
│ ⭐ 4.9/5.0           │ Sarah logged:        │                  │
│ [Manage]             │ Morning meds given   │ [🧑‍⚕️ Caregiver]  │
│                      │ [View photo]         │ Sarah on duty    │
│ Location:            │                      │ 9am-12pm         │
│ 🏠 Home (safe)       │ 9:58 AM              │                  │
│ [History]            │ Dorothy scanned      │ [⚙️ Settings]    │
│                      │ food label           │                  │
│ AI Chats:            │ [View analysis]      │ [📊 Reports]     │
│ 43 interactions      │                      │                  │
│ [Review]             │ 9:35 AM              │                  │
│                      │ Breakfast completed  │                  │
│ ⚠️ ALERTS (2)        │ (Logged by Sarah)    │                  │
│                      │                      │                  │
│ • Missed dose        │ 9:03 AM              │                  │
│   yesterday 8pm      │ Sarah arrived        │                  │
│   [Details]          │ (On time ✓)          │                  │
│                      │                      │                  │
│ • Confusion pattern  │ [Load More]          │                  │
│   detected           │ [Filter Activity]    │                  │
│   [Review]           │                      │                  │
│                      │                      │                  │
│ 📅 TODAY'S SCHEDULE  │                      │ 📈 THIS WEEK     │
│                      │                      │                  │
│ 9:00 AM ✓           │                      │ Sessions: 12     │
│ Sarah arrives        │                      │ Hours: 36        │
│                      │                      │ Cost: $900       │
│ 2:00 PM              │                      │                  │
│ Doctor appointment   │                      │ [View Budget]    │
│ Dr. Johnson          │                      │                  │
│ [Directions]         │                      │                  │
│                      │                      │                  │
│ 7:00 PM              │                      │                  │
│ Evening medication   │                      │                  │
│ [Set Reminder]       │                      │                  │
└──────────────────────┴──────────────────────┴──────────────────┘

[Below - Full Width Analytics]

┌─────────────────────────────────────────────────────────────────┐
│ 📊 INSIGHTS & TRENDS                      [This Month ▼]       │
│                                                                 │
│ [Tab: Medications] [Health] [Activity] [Conversations] [Costs] │
│                                                                 │
│ Medication Adherence (Last 30 Days)                            │
│ [LINE CHART showing adherence % over time]                     │
│ Overall: 94% ✓ Target: >90%                                    │
│                                                                 │
│ ⚠️ Pattern detected: Evening doses missed 5 times              │
│ 💡 Recommendation: Adjust reminder volume/timing               │
│                                                                 │
│ [View Full Report] [Share with Doctor] [Adjust Settings]       │
└─────────────────────────────────────────────────────────────────┘
```

---

#### Screen 2: PATIENT MANAGEMENT (Detailed)

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard                                            │
│                                                                 │
│  Patient Profile: Dorothy Martinez                             │
│  [Edit] [Share Access] [Download Data] [Print]                 │
└─────────────────────────────────────────────────────────────────┘

[Tabs]
Overview | Medical | Caregivers | Settings | Access | Billing

---

[Overview Tab - Multi-Column]

┌──────────────────────┬──────────────────────────────────────────┐
│ BASIC INFORMATION    │ DIAGNOSIS & CARE LEVEL                   │
├──────────────────────┼──────────────────────────────────────────┤
│ Name: Dorothy M.     │ Primary Diagnosis:                       │
│ Age: 78              │ Early-stage Alzheimer's disease          │
│ DOB: 03/15/1947      │ Diagnosed: June 2023                     │
│                      │ Neurologist: Dr. Anderson                │
│ Address:             │                                          │
│ 123 Oak Street       │ Current Care Level: 2 (Moderate)         │
│ San Francisco, CA    │ [View Assessment] [Update]               │
│                      │                                          │
│ Phone:               │ Secondary Conditions:                    │
│ (415) 555-0123       │ • Hypertension (controlled)              │
│                      │ • Osteoarthritis (mild)                  │
│ Email:               │                                          │
│ dorothy.m@email.com  │ Allergies:                               │
│ (Monitored by you)   │ ⚠️ Dairy (severe - anaphylaxis risk)     │
│                      │ ⚠️ Penicillin                            │
│ [Edit Info]          │                                          │
│                      │ [Add Medical Record]                     │
└──────────────────────┴──────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 💊 CURRENT MEDICATIONS (4 active)               [Add Med] [Edit]│
│                                                                 │
│ [Medication Card]                                               │
│ ┌─────────────┬───────────────────────────────────────────────┐│
│ │ [PHOTO]     │ Donepezil (Aricept) 10mg                      ││
│ │ White pill  │ Schedule: Once daily at 9:00 AM               ││
│ │             │ Purpose: Alzheimer's disease management       ││
│ │             │ Prescribing Doctor: Dr. Anderson              ││
│ │             │ Pharmacy: Walgreens #4521                     ││
│ │             │ Refills remaining: 2                          ││
│ │             │ Next refill: Jan 28, 2025                     ││
│ │             │                                               ││
│ │             │ Adherence (7 days): ✅✅✅✅✅✅❌ (86%)        ││
│ │             │ ⚠️ Missed: Jan 14 (evening)                   ││
│ │             │                                               ││
│ │             │ [View History] [Edit] [Discontinue]           ││
│ └─────────────┴───────────────────────────────────────────────┘│
│                                                                 │
│ [3 more medication cards...]                                    │
│                                                                 │
│ 💡 AI Insight: No interactions detected between current meds   │
│ ✓ All medications appropriate for diagnosis                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 📞 EMERGENCY CONTACTS & CARE TEAM                               │
│                                                                 │
│ Primary Contact: You (Sarah Martinez - Daughter)                │
│ Phone: (415) 555-0199 | Email: sarah.m@email.com               │
│ Notification Preferences: ✓ SMS ✓ Email ✓ App                  │
│                                                                 │
│ Secondary Contact: Michael Martinez (Son)                       │
│ Phone: (310) 555-0145 | Email: michael.m@email.com             │
│ Notification Preferences: ✓ Email ✓ App (SMS emergencies only) │
│ Access Level: View Only                                        │
│                                                                 │
│ Healthcare Providers:                                           │
│ • Dr. Sarah Johnson (Primary Care)     📞 (415) 555-0100       │
│ • Dr. Robert Anderson (Neurology)      📞 (415) 555-0200       │
│ • Walgreens Pharmacy #4521             📞 (415) 555-0300       │
│                                                                 │
│ [Add Contact] [Edit Notifications] [Manage Access]              │
└─────────────────────────────────────────────────────────────────┘

---

[Medical Tab - Detailed Health Records]

┌─────────────────────────────────────────────────────────────────┐
│ 🏥 MEDICAL RECORDS & HISTORY                                    │
│                                                                 │
│ [Upload New] [Import from Provider] [Request Records]          │
│                                                                 │
│ Recent Visits:                                                  │
│                                                                 │
│ Jan 10, 2025 - Dr. Johnson (Primary Care) - Regular checkup    │
│ [View Notes] [View Test Results] [Download]                    │
│ Summary: Blood pressure controlled, minor weight loss noted    │
│                                                                 │
│ Dec 15, 2024 - Dr. Anderson (Neurology) - 6-month follow-up    │
│ [View Notes] [View MRI Results]                                │
│ Summary: Condition stable, continue current medications        │
│                                                                 │
│ [View Full Medical History]                                     │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ Immunizations:                                                  │
│ ✓ Flu shot (Oct 2024)                                          │
│ ✓ COVID-19 booster (Nov 2024)                                  │
│ ⚠️ Pneumonia vaccine due (Recommended for age)                 │
│                                                                 │
│ [View Immunization Records] [Schedule Vaccines]                 │
└─────────────────────────────────────────────────────────────────┘

---

[Caregivers Tab - Management]

┌─────────────────────────────────────────────────────────────────┐
│ 🧑‍⚕️ CAREGIVER MANAGEMENT                                        │
│                                                                 │
│ Active Caregivers (2):                [Find New] [View History] │
│                                                                 │
│ [Caregiver Card - Expanded]                                     │
│ ┌───────────────────────────────────────────────────────────┐  │
│ │ [PROFILE PHOTO]    Sarah K. ⭐ 4.9/5.0 (128 reviews)       │  │
│ │                                                           │  │
│ │ Certification: Level 3 (Advanced Medical)                 │  │
│ │ Specializations:                                          │  │
│ │ • Dementia Care Specialist ✓                              │  │
│ │ • CPR/First Aid (Exp. 06/2025) ✓                          │  │
│ │ • Medication Administration ✓                             │  │
│ │                                                           │  │
│ │ Experience: 8 years | Platform: 500+ hours                │  │
│ │ Background Check: ✓ Verified (Dec 2024)                   │  │
│ │                                                           │  │
│ │ Schedule with Dorothy:                                    │  │
│ │ Monday, Wednesday, Friday: 9:00 AM - 12:00 PM             │  │
│ │ (12 hours/week)                                           │  │
│ │                                                           │  │
│ │ Rate: $25/hour ($300/week, $1,200/month)                  │  │
│ │                                                           │  │
│ │ Performance (Last 30 days):                               │  │
│ │ • On-time: 100% (12/12 sessions)                          │  │
│ │ • Task completion: 100%                                   │  │
│ │ • Your rating: ⭐⭐⭐⭐⭐ (All 5-star reviews)              │  │
│ │ • Mom's comfort level: High                               │  │
│ │   (Low confusion, positive mood after visits)             │  │
│ │                                                           │  │
│ │ Your Notes:                                               │  │
│ │ "Sarah is wonderful. Mom remembers her name and looks     │  │
│ │  forward to her visits. Very professional and caring."    │  │
│ │                                                           │  │
│ │ [💬 Message] [📞 Call] [📅 Adjust Schedule]               │  │
│ │ [📊 View Full Stats] [⚙️ Settings] [⛔ End Contract]       │  │
│ └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│ [Second Caregiver Card - Robert M.]                             │
│ ...                                                             │
└─────────────────────────────────────────────────────────────────┘

---

[Settings Tab - Comprehensive Control]

┌─────────────────────────────────────────────────────────────────┐
│ ⚙️ PATIENT SETTINGS & PREFERENCES                               │
│                                                                 │
│ [Sections - Expandable]                                         │
│                                                                 │
│ ▼ AI ASSISTANT CONFIGURATION                                    │
│                                                                 │
│   Voice & Speech:                                               │
│   Voice: [Samantha (US Female) ▼]                              │
│   Speech Rate: [●-------] 0.85x (Slower for clarity)           │
│   Volume: [-----●---] 75%                                       │
│   [🔊 Test Voice]                                               │
│                                                                 │
│   Personality & Tone:                                           │
│   Formality: ◯ Formal  ● Warm & Friendly  ◯ Casual             │
│   Address as: [Dorothy ▼] (First name / Mrs. Martinez)         │
│   Repetition handling:                                          │
│   ☑ Never say "I already told you this"                        │
│   ☑ Patiently repeat information                               │
│   ☑ Simplify explanation on third repetition                   │
│                                                                 │
│   Language:                                                     │
│   Primary: [English (US) ▼]                                    │
│   Secondary: [Spanish ▼] (If needed)                           │
│   Reading Level: [5th Grade ▼] (Simple language)               │
│                                                                 │
│   [Save Changes]                                                │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ ▼ PERMISSIONS & ACCESS CONTROL                                  │
│                                                                 │
│   Dorothy can:                                                  │
│   ✓ Talk to AI assistant (unlimited)                           │
│   ✓ View calendar and schedule                                 │
│   ✓ See messages from family/caregivers                        │
│   ✓ Take photos for analysis                                   │
│   ✓ Call emergency contacts                                    │
│   ✓ Rate caregivers (simple thumbs up/down)                    │
│                                                                 │
│   Dorothy needs approval for:                                   │
│   ☑ Replying to messages                                       │
│   ☑ Requesting new caregivers                                  │
│   ☑ Changing schedule                                          │
│                                                                 │
│   Dorothy cannot:                                               │
│   ☑ View financial information                                 │
│   ☑ Delete care logs or history                                │
│   ☑ Change medications                                         │
│   ☑ Remove caregivers                                          │
│   ☑ Access settings                                            │
│                                                                 │
│   [Customize Permissions]                                       │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ ▼ LOCATION & SAFETY                                             │
│                                                                 │
│   Location Tracking:                                            │
│   ● Enabled  ◯ Disabled                                         │
│   Update Frequency: [Every 5 minutes ▼]                        │
│   Battery Optimization: ☑ Use power-saving mode                │
│                                                                 │
│   Geofences (3 active):                                         │
│                                                                 │
│   1. 🏠 Home (123 Oak St)                                       │
│      Radius: [100] meters                                       │
│      Alert on: ◯ Entry  ● Exit  ☑ Night exit (10pm-6am)       │
│      Notify: [You, Michael ▼]                                  │
│      [Edit] [Delete]                                            │
│                                                                 │
│   2. 🏥 Senior Center (456 Pine Ave)                            │
│      Radius: [50] meters                                        │
│      Alert on: ● Entry  ● Exit  ◯ Time-based                   │
│      Notify: [You ▼]                                           │
│      [Edit] [Delete]                                            │
│                                                                 │
│   3. 🏠 Your House (789 Elm Rd)                                 │
│      Radius: [100] meters                                       │
│      Alert on: ● Entry  ◯ Exit                                 │
│      Notify: [You ▼]                                           │
│      [Edit] [Delete]                                            │
│                                                                 │
│   [+ Add New Geofence]                                          │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ ▼ NOTIFICATIONS & ALERTS                                        │
│                                                                 │
│   Recipients: (Who gets alerts?)                                │
│   ☑ You (Sarah) - All alerts                                   │
│     Methods: ☑ SMS  ☑ Email  ☑ App Push                        │
│   ☑ Michael (Brother) - Emergencies only                       │
│     Methods: ☑ Email  ☑ App Push                               │
│                                                                 │
│   Alert Types:                                                  │
│   ☑ Medication missed (>30 min late)                           │
│   ☑ Geofence alerts (entry/exit from safe zones)               │
│   ☑ Unusual location (outside known areas)                     │
│   ☑ Night activity (10pm-6am)                                  │
│   ☑ Caregiver late (>15 min)                                   │
│   ☑ Caregiver didn't show up                                   │
│   ☑ Confusion indicators (AI detected repetitive questions)    │
│   ☑ Emergency keywords ("help", "fell", "hurt")                │
│   ☑ Low phone battery (<20%)                                   │
│   ☐ Daily summary email (end of day)                           │
│   ☐ Weekly report (Sunday evening)                             │
│                                                                 │
│   Quiet Hours: (Reduce non-emergency alerts)                   │
│   ☑ Enabled                                                     │
│   Time: [10:00 PM] to [7:00 AM]                                │
│   Emergency alerts still sent: ☑ Yes                           │
│                                                                 │
│   [Save Notification Settings]                                  │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ ▼ BILLING & BUDGET                                              │
│                                                                 │
│   Payment Method:                                               │
│   💳 Visa ending in 1234 (Exp. 06/2026)                        │
│   [Update Card] [Add Bank Account] [Billing History]           │
│                                                                 │
│   Automatic Payments:                                           │
│   ● Enabled (Recommended) ◯ Manual approval required           │
│   Frequency: [Weekly ▼] (Every Friday)                         │
│                                                                 │
│   Budget & Spending:                                            │
│   Monthly Budget: $[2,000]                                      │
│   Alert when: [80]% spent (Email + SMS)                        │
│   Hard cap: ☐ Stop services if budget exceeded                 │
│             ☑ Allow overage, notify me                         │
│                                                                 │
│   Current Month (January):                                      │
│   Spent: $1,450 / $2,000 (72.5%)                               │
│   Remaining: $550 (Est. 5 more days of care)                   │
│   [View Detailed Breakdown]                                     │
│                                                                 │
│   Estimated Next Month:                                         │
│   Based on current schedule: ~$1,800                           │
│   [Adjust Budget] [Modify Schedule]                            │
│                                                                 │
│   [Download Invoices] [Tax Documents]                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

#### Screen 3: ANALYTICS & INSIGHTS

```
┌─────────────────────────────────────────────────────────────────┐
│  📊 Analytics & Health Insights - Dorothy Martinez              │
│  [Date Range: Last 30 Days ▼] [Compare to: Previous Month]     │
│  [Export Report] [Share with Doctor] [Print]                   │
└─────────────────────────────────────────────────────────────────┘

[Tab Navigation]
Overview | Medications | Activity | Conversations | Caregivers | Costs

---

[Overview Tab]

┌──────────────────────┬──────────────────────┬──────────────────┐
│ HEALTH METRICS       │ CARE QUALITY         │ WELLBEING        │
├──────────────────────┼──────────────────────┼──────────────────┤
│                      │                      │                  │
│ Medication Adherence │ Caregiver Rating     │ Mood Trend       │
│                      │                      │                  │
│   [94%] ↓ -2%        │   [4.9] → same       │   [😊] ↑ Better  │
│                      │                      │                  │
│ ✅ 67/70 doses       │ ⭐⭐⭐⭐⭐            │ Positive: 78%    │
│ ❌ 3 missed          │                      │ Neutral: 18%     │
│                      │ All 5-star reviews   │ Negative: 4%     │
│ [View Details]       │ this month           │                  │
│                      │                      │ [Analysis]       │
│                      │ [View Feedback]      │                  │
└──────────────────────┴──────────────────────┴──────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 💊 MEDICATION ADHERENCE (30 Days)                               │
│                                                                 │
│ [LINE CHART: Daily adherence percentage over time]             │
│                                                                 │
│ 100% ┤     ●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●       │
│      ┤                                                         │
│  95% ┤                                         ○               │
│      ┤                                                         │
│  90% ┤                 ○                   ○       ○           │
│      ┤                                                         │
│  85% ┤                     ○                                   │
│      └────────────────────────────────────────────────────────→│
│       Dec 15        Jan 1          Jan 15          Jan 30      │
│                                                                 │
│ ⚠️ PATTERNS DETECTED:                                           │
│ • Evening doses most frequently missed (5 times)                │
│ • Perfect adherence on caregiver visit days (Mon/Wed/Fri)      │
│ • Weekends show lower adherence (-8%)                          │
│                                                                 │
│ 💡 RECOMMENDATIONS:                                             │
│ ✓ Consider weekend caregiver coverage                          │
│ ✓ Adjust evening reminder (louder, different sound)            │
│ ✓ Visual pill organizer for weekends                           │
│                                                                 │
│ [Accept Recommendations] [Dismiss] [Customize]                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 📍 LOCATION & ACTIVITY PATTERNS                                 │
│                                                                 │
│ [HEAT MAP: Where Dorothy spends time]                          │
│                                                                 │
│ Time Breakdown:                                                 │
│ 🏠 Home: 85% (20.4 hrs/day)                                     │
│ 🏥 Senior Center: 8% (2 hrs/day, Mon/Thu)                       │
│ 🏠 Your House: 5% (1-2 hrs/day, weekends)                       │
│ 🏪 Other locations: 2% (errands with caregiver)                 │
│                                                                 │
│ [MAP VIEW]  [TIMELINE VIEW]  [Export Data]                      │
│                                                                 │
│ ✓ No unusual locations detected                                │
│ ✓ All travel with caregiver or family present                  │
│ ✓ No nighttime wandering incidents                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 🗣️ AI CONVERSATION ANALYSIS (43 interactions)                   │
│                                                                 │
│ Most Frequent Questions:                                        │
│ 1. "What day is it?" (18 times) ⚠️ Increased from last month   │
│ 2. "When is Sarah coming?" (12 times)                          │
│ 3. "What pills do I take?" (8 times)                            │
│ 4. "What's for lunch/dinner?" (7 times)                         │
│                                                                 │
│ Topics Discussed:                                               │
│ • Medications: 35% │ • Calendar/Time: 30% │ • Family: 20% │   │
│ • Food: 10%        │ • Other: 5%                              │
│                                                                 │
│ ⚠️ COGNITIVE INDICATORS:                                        │
│ • Time disorientation: Increased (15 instances)                 │
│ • Repetitive questions: Up 25% from last month                  │
│ • Word-finding difficulty: 3 instances                          │
│                                                                 │
│ 💡 RECOMMENDATION:                                              │
│ Consider discussing cognitive changes with Dr. Anderson at      │
│ next appointment (Feb 10). Possible care level reassessment.    │
│                                                                 │
│ [View Full Transcript] [Share with Doctor] [Schedule Appt]      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 💵 CARE COSTS & BUDGET                                          │
│                                                                 │
│ [BAR CHART: Weekly spending]                                    │
│                                                                 │
│ $500 ┤                                 ████                     │
│     ┤                                 ████                     │
│ $400 ┤                 ████            ████   ████             │
│     ┤                 ████            ████   ████             │
│ $300 ┤     ████        ████   ████    ████   ████             │
│     ┤     ████        ████   ████    ████   ████             │
│ $200 ┤     ████        ████   ████    ████   ████             │
│     ┤     ████        ████   ████    ████   ████             │
│ $100 ┤     ████        ████   ████    ████   ████             │
│     └────────────────────────────────────────────────────────→ │
│      Wk 1   Wk 2   Wk 3   Wk 4   Wk 5 (partial)               │
│      $300   $450   $375   $450   $125                          │
│                                                                 │
│ Month Total: $1,700 / $2,000 budget (85%)                      │
│ Average per session: $75                                        │
│ Average hourly rate: $25                                        │
│                                                                 │
│ Breakdown by Caregiver:                                         │
│ • Sarah K.: $1,200 (70%) - 12 sessions, 48 hours               │
│ • Robert M.: $500 (30%) - 6 sessions, 20 hours                 │
│                                                                 │
│ [View Invoices] [Adjust Budget] [Download Tax Summary]          │
└─────────────────────────────────────────────────────────────────┘

[Export Options at Bottom]
┌─────────────────────────────────────────────────────────────────┐
│ 📄 GENERATE REPORT                                              │
│                                                                 │
│ Report Type: [Healthcare Provider Summary ▼]                   │
│ • Healthcare Provider Summary (PDF)                             │
│ • Monthly Care Summary (PDF)                                    │
│ • Medication Adherence Report (PDF/Excel)                       │
│ • Complete Data Export (JSON/CSV)                               │
│ • Insurance Documentation (PDF)                                 │
│                                                                 │
│ Date Range: [Last 30 Days ▼]                                   │
│ Include: ☑ Medications ☑ Appointments ☑ Caregiver Notes        │
│          ☑ Location History ☑ AI Conversations                 │
│                                                                 │
│ [Generate & Download] [Email to Doctor] [Print]                 │
└─────────────────────────────────────────────────────────────────┘
```

---

This is comprehensive but I'm hitting message limits. Let me summarize the key points and next steps for you.
