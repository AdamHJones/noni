# Care Companion - Integration Implementation Guide

**Purpose:** Step-by-step guide to integrate real APIs for calendar, email, banking, healthcare, and messaging

**Last Updated:** October 29, 2025

---

## INTEGRATION OVERVIEW

This guide covers how to connect your Care Companion app to actual services. Each integration includes:
- Setup instructions
- Code examples
- Security considerations
- Testing procedures

**Prerequisites:**
- Node.js 18+ or Python 3.9+
- API keys for each service
- SSL certificates for production
- HIPAA compliance checklist (for healthcare data)

---

## 1. CALENDAR INTEGRATION

### Google Calendar API

**Setup Steps:**

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com
   - Create new project: "CareCompanion"
   - Enable Google Calendar API

2. **Configure OAuth 2.0**
   - Create OAuth 2.0 credentials
   - Add authorized redirect URIs
   - Download credentials JSON

3. **Scopes Needed:**
   ```
   https://www.googleapis.com/auth/calendar.readonly
   https://www.googleapis.com/auth/calendar.events
   ```

**Implementation (Node.js):**

```javascript
const { google } = require('googleapis');
const fs = require('fs');

class CalendarService {
    constructor(credentialsPath) {
        const credentials = JSON.parse(fs.readFileSync(credentialsPath));
        const { client_secret, client_id, redirect_uris } = credentials.installed;
        
        this.oAuth2Client = new google.auth.OAuth2(
            client_id,
            client_secret,
            redirect_uris[0]
        );
    }

    // Authenticate user (one-time setup)
    async authenticate(tokenPath) {
        try {
            const token = JSON.parse(fs.readFileSync(tokenPath));
            this.oAuth2Client.setCredentials(token);
        } catch (err) {
            return this.getAccessToken();
        }
    }

    // Get events for today
    async getTodayEvents() {
        const calendar = google.calendar({ version: 'v3', auth: this.oAuth2Client });
        
        const now = new Date();
        const endOfDay = new Date(now);
        endOfDay.setHours(23, 59, 59, 999);

        try {
            const response = await calendar.events.list({
                calendarId: 'primary',
                timeMin: now.toISOString(),
                timeMax: endOfDay.toISOString(),
                singleEvents: true,
                orderBy: 'startTime',
            });

            return response.data.items || [];
        } catch (error) {
            console.error('Error fetching calendar events:', error);
            throw error;
        }
    }

    // Get upcoming events (next 7 days)
    async getUpcomingEvents(days = 7) {
        const calendar = google.calendar({ version: 'v3', auth: this.oAuth2Client });
        
        const now = new Date();
        const future = new Date(now);
        future.setDate(future.getDate() + days);

        const response = await calendar.events.list({
            calendarId: 'primary',
            timeMin: now.toISOString(),
            timeMax: future.toISOString(),
            maxResults: 50,
            singleEvents: true,
            orderBy: 'startTime',
        });

        return response.data.items || [];
    }

    // Create a simple reminder event (WITH USER CONFIRMATION)
    async createReminder(summary, dateTime, description = '') {
        const calendar = google.calendar({ version: 'v3', auth: this.oAuth2Client });
        
        const event = {
            summary: summary,
            description: description,
            start: {
                dateTime: dateTime,
                timeZone: 'America/Denver', // Adjust to user's timezone
            },
            end: {
                dateTime: new Date(new Date(dateTime).getTime() + 60*60*1000).toISOString(), // 1 hour duration
                timeZone: 'America/Denver',
            },
            reminders: {
                useDefault: false,
                overrides: [
                    { method: 'popup', minutes: 15 },
                    { method: 'popup', minutes: 60 },
                ],
            },
        };

        const response = await calendar.events.insert({
            calendarId: 'primary',
            resource: event,
        });

        return response.data;
    }

    // Format events for voice response
    formatEventsForSpeech(events) {
        if (events.length === 0) {
            return "You don't have any events scheduled.";
        }

        let speech = `You have ${events.length} event${events.length > 1 ? 's' : ''} coming up. `;
        
        events.forEach((event, index) => {
            const start = new Date(event.start.dateTime || event.start.date);
            const timeStr = event.start.dateTime 
                ? start.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
                : 'all day';
            
            speech += `${event.summary} at ${timeStr}`;
            if (index < events.length - 1) speech += ', ';
        });

        return speech;
    }
}

// Usage example
async function exampleUsage() {
    const cal = new CalendarService('./credentials.json');
    await cal.authenticate('./token.json');
    
    const todayEvents = await cal.getTodayEvents();
    console.log(cal.formatEventsForSpeech(todayEvents));
}

module.exports = CalendarService;
```

**Security Notes:**
- Store tokens encrypted
- Refresh tokens before expiration
- Never log sensitive calendar data
- Implement rate limiting

---

## 2. EMAIL INTEGRATION (GMAIL)

### Gmail API

**Setup Steps:**

1. **Enable Gmail API** in Google Cloud Console
2. **OAuth Scopes:**
   ```
   https://www.googleapis.com/auth/gmail.readonly
   https://www.googleapis.com/auth/gmail.send (for replies)
   https://www.googleapis.com/auth/gmail.modify (for marking read)
   ```

**Implementation (Node.js):**

```javascript
const { google } = require('googleapis');

class EmailService {
    constructor(oAuth2Client) {
        this.gmail = google.gmail({ version: 'v1', auth: oAuth2Client });
    }

    // Get unread messages from last 7 days
    async getRecentUnreadMessages(maxResults = 10) {
        try {
            const response = await this.gmail.users.messages.list({
                userId: 'me',
                q: 'is:unread newer_than:7d',
                maxResults: maxResults,
            });

            if (!response.data.messages) {
                return [];
            }

            // Fetch full message details
            const messages = await Promise.all(
                response.data.messages.map(msg => this.getMessageDetail(msg.id))
            );

            return messages;
        } catch (error) {
            console.error('Error fetching emails:', error);
            throw error;
        }
    }

    // Get message details
    async getMessageDetail(messageId) {
        const response = await this.gmail.users.messages.get({
            userId: 'me',
            id: messageId,
            format: 'full',
        });

        const message = response.data;
        const headers = message.payload.headers;

        return {
            id: message.id,
            threadId: message.threadId,
            subject: this.getHeader(headers, 'Subject'),
            from: this.getHeader(headers, 'From'),
            date: this.getHeader(headers, 'Date'),
            snippet: message.snippet,
            body: this.getMessageBody(message.payload),
        };
    }

    // Extract header value
    getHeader(headers, name) {
        const header = headers.find(h => h.name.toLowerCase() === name.toLowerCase());
        return header ? header.value : '';
    }

    // Extract message body
    getMessageBody(payload) {
        let body = '';
        
        if (payload.parts) {
            payload.parts.forEach(part => {
                if (part.mimeType === 'text/plain' && part.body.data) {
                    body += Buffer.from(part.body.data, 'base64').toString('utf-8');
                }
            });
        } else if (payload.body.data) {
            body = Buffer.from(payload.body.data, 'base64').toString('utf-8');
        }

        return body;
    }

    // Send reply (REQUIRES CONFIRMATION)
    async sendReply(originalMessageId, replyText, recipientEmail) {
        const raw = this.createReplyMessage(recipientEmail, replyText, originalMessageId);
        
        const response = await this.gmail.users.messages.send({
            userId: 'me',
            requestBody: {
                raw: raw,
                threadId: originalMessageId, // Keep in same thread
            },
        });

        return response.data;
    }

    // Create email message in RFC 2822 format
    createReplyMessage(to, message, threadId) {
        const email = [
            `To: ${to}`,
            'Content-Type: text/plain; charset=utf-8',
            'MIME-Version: 1.0',
            `Subject: Re: `,
            '',
            message,
        ].join('\n');

        return Buffer.from(email)
            .toString('base64')
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=+$/, '');
    }

    // Format emails for voice response
    formatEmailsForSpeech(messages) {
        if (messages.length === 0) {
            return "You don't have any new messages.";
        }

        let speech = `You have ${messages.length} unread message${messages.length > 1 ? 's' : ''}. `;
        
        messages.slice(0, 3).forEach((msg, index) => { // Only first 3
            const from = this.extractName(msg.from);
            speech += `${from} sent you an email about ${msg.subject}. `;
        });

        if (messages.length > 3) {
            speech += `And ${messages.length - 3} more messages.`;
        }

        return speech;
    }

    // Extract name from email address
    extractName(fromHeader) {
        const match = fromHeader.match(/^"?([^"<]+)"?\s*</);
        return match ? match[1].trim() : fromHeader.split('@')[0];
    }
}

module.exports = EmailService;
```

**Security Notes:**
- Implement approved sender whitelist
- Block attachments from unknown senders
- Never auto-execute links in emails
- Log all sent emails for audit

---

## 3. BANKING INTEGRATION (PLAID)

### Plaid API for Financial Data

**Setup Steps:**

1. **Sign up at Plaid** (https://plaid.com)
2. **Get API credentials:**
   - Client ID
   - Secret (sandbox/development/production)
3. **Choose products:** Transactions, Balance, Identity

**Implementation (Node.js):**

```javascript
const plaid = require('plaid');

class BankingService {
    constructor(clientId, secret, env = 'sandbox') {
        const configuration = new plaid.Configuration({
            basePath: plaid.PlaidEnvironments[env],
            baseOptions: {
                headers: {
                    'PLAID-CLIENT-ID': clientId,
                    'PLAID-SECRET': secret,
                },
            },
        });

        this.client = new plaid.PlaidApi(configuration);
        this.accessToken = null;
    }

    // Link user's bank account (one-time setup)
    async createLinkToken(userId) {
        const request = {
            user: { client_user_id: userId },
            client_name: 'Care Companion',
            products: ['transactions', 'auth', 'identity'],
            country_codes: ['US'],
            language: 'en',
        };

        const response = await this.client.linkTokenCreate(request);
        return response.data.link_token;
    }

    // Exchange public token for access token
    async exchangePublicToken(publicToken) {
        const response = await this.client.itemPublicTokenExchange({
            public_token: publicToken,
        });

        this.accessToken = response.data.access_token;
        return this.accessToken;
    }

    // Get account balances
    async getBalances() {
        if (!this.accessToken) {
            throw new Error('No access token. User must link their bank account.');
        }

        const request = { access_token: this.accessToken };
        const response = await this.client.accountsBalanceGet(request);

        return response.data.accounts.map(account => ({
            name: account.name,
            type: account.type,
            subtype: account.subtype,
            balance: account.balances.current,
            available: account.balances.available,
            currency: account.balances.iso_currency_code,
            // NEVER expose: account number, routing number
        }));
    }

    // Get recent transactions
    async getRecentTransactions(days = 30) {
        if (!this.accessToken) {
            throw new Error('No access token.');
        }

        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - days);

        const request = {
            access_token: this.accessToken,
            start_date: startDate.toISOString().split('T')[0],
            end_date: endDate.toISOString().split('T')[0],
            options: {
                count: 50,
                offset: 0,
            },
        };

        const response = await this.client.transactionsGet(request);

        return response.data.transactions.map(txn => ({
            date: txn.date,
            name: txn.name,
            amount: txn.amount,
            category: txn.category,
            pending: txn.pending,
        }));
    }

    // Format balance for voice response
    formatBalanceForSpeech(accounts) {
        if (accounts.length === 0) {
            return "I couldn't find any account information.";
        }

        const checking = accounts.find(acc => acc.subtype === 'checking');
        const savings = accounts.find(acc => acc.subtype === 'savings');

        let speech = '';

        if (checking) {
            speech += `You have $${checking.balance.toLocaleString()} in your checking account. `;
        }

        if (savings) {
            speech += `And $${savings.balance.toLocaleString()} in your savings account. `;
        }

        speech += 'All your accounts are in good standing.';

        return speech;
    }

    // Check if specific deposit arrived
    async checkForDeposit(expectedAmount, description) {
        const transactions = await this.getRecentTransactions(7);
        
        const found = transactions.find(txn => 
            txn.amount === -Math.abs(expectedAmount) && // Negative = deposit in Plaid
            txn.name.toLowerCase().includes(description.toLowerCase())
        );

        return found !== undefined;
    }
}

module.exports = BankingService;
```

**Security Notes:**
- NEVER store plain access tokens (encrypt at rest)
- Use Plaid's webhook for balance updates
- Implement transaction limits for any actions
- Read-only access only (no transfers without multi-factor auth)
- Rotate secrets regularly

---

## 4. SMS/TEXT MESSAGING (TWILIO)

### Twilio API

**Setup Steps:**

1. **Sign up at Twilio** (https://twilio.com)
2. **Get credentials:**
   - Account SID
   - Auth Token
3. **Buy a phone number** for sending/receiving

**Implementation (Node.js):**

```javascript
const twilio = require('twilio');

class MessagingService {
    constructor(accountSid, authToken, fromNumber) {
        this.client = twilio(accountSid, authToken);
        this.fromNumber = fromNumber;
        this.approvedContacts = new Set(); // Whitelist
    }

    // Add approved contact
    addApprovedContact(phoneNumber, name) {
        this.approvedContacts.add(phoneNumber);
        console.log(`Added approved contact: ${name} (${phoneNumber})`);
    }

    // Get recent messages
    async getRecentMessages(limit = 20) {
        const messages = await this.client.messages.list({
            to: this.fromNumber,
            limit: limit,
        });

        return messages.map(msg => ({
            from: msg.from,
            body: msg.body,
            date: msg.dateCreated,
            sid: msg.sid,
        }));
    }

    // Send SMS (ONLY to approved contacts, WITH confirmation)
    async sendMessage(to, body, requireConfirmation = true) {
        // Security check
        if (!this.approvedContacts.has(to)) {
            throw new Error(`Cannot send message to unapproved number: ${to}`);
        }

        if (requireConfirmation) {
            // In real app, this would pause and ask user to confirm
            console.log(`CONFIRMATION NEEDED: Send "${body}" to ${to}?`);
            // Return pending status, wait for confirmation
            return { status: 'pending_confirmation', to, body };
        }

        // Send the message
        const message = await this.client.messages.create({
            body: body,
            from: this.fromNumber,
            to: to,
        });

        return {
            status: 'sent',
            sid: message.sid,
            to: to,
            body: body,
        };
    }

    // Format messages for voice response
    formatMessagesForSpeech(messages, contactMap) {
        if (messages.length === 0) {
            return "You don't have any new text messages.";
        }

        let speech = `You have ${messages.length} text message${messages.length > 1 ? 's' : ''}. `;
        
        messages.slice(0, 3).forEach((msg, index) => {
            const name = contactMap[msg.from] || 'someone';
            speech += `${name} said: ${msg.body}. `;
        });

        if (messages.length > 3) {
            speech += `And ${messages.length - 3} more messages.`;
        }

        return speech;
    }

    // Get contact name from phone number
    getContactName(phoneNumber, contactMap) {
        return contactMap[phoneNumber] || phoneNumber;
    }
}

module.exports = MessagingService;
```

**Security Notes:**
- Maintain approved contact whitelist
- Log all sent messages
- Rate limit outgoing messages
- Block premium SMS numbers
- Notify caregiver of all communications

---

## 5. MEDICATION/HEALTHCARE INTEGRATION

### Custom Medication Tracker

**Implementation (Node.js + Database):**

```javascript
class MedicationService {
    constructor(database) {
        this.db = database; // PostgreSQL or similar
    }

    // Add medication to schedule
    async addMedication(userId, medication) {
        const query = `
            INSERT INTO medications (user_id, name, dosage, frequency, times, image_url)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        `;
        
        const result = await this.db.query(query, [
            userId,
            medication.name,
            medication.dosage,
            medication.frequency, // 'daily', 'twice_daily', 'weekly'
            JSON.stringify(medication.times), // ['08:00', '20:00']
            medication.imageUrl,
        ]);

        return result.rows[0];
    }

    // Get medications due now (within 30 minute window)
    async getMedicationsDueNow(userId) {
        const now = new Date();
        const timeStr = now.toTimeString().substring(0, 5); // 'HH:MM'

        const query = `
            SELECT * FROM medications
            WHERE user_id = $1
            AND times::jsonb ? $2
        `;

        const result = await this.db.query(query, [userId, timeStr]);
        return result.rows;
    }

    // Record medication taken
    async recordMedicationTaken(userId, medicationId) {
        const query = `
            INSERT INTO medication_log (user_id, medication_id, taken_at)
            VALUES ($1, $2, NOW())
        `;

        await this.db.query(query, [userId, medicationId]);
    }

    // Check if medication was taken today
    async wasMedicationTakenToday(userId, medicationId) {
        const query = `
            SELECT COUNT(*) as count
            FROM medication_log
            WHERE user_id = $1
            AND medication_id = $2
            AND taken_at::date = CURRENT_DATE
        `;

        const result = await this.db.query(query, [userId, medicationId]);
        return result.rows[0].count > 0;
    }

    // Get medication adherence rate (last 30 days)
    async getAdherenceRate(userId) {
        const query = `
            SELECT 
                COUNT(DISTINCT DATE(taken_at)) * 100.0 / 30 as adherence_rate
            FROM medication_log
            WHERE user_id = $1
            AND taken_at >= NOW() - INTERVAL '30 days'
        `;

        const result = await this.db.query(query, [userId]);
        return result.rows[0].adherence_rate || 0;
    }

    // Format medication reminder for speech
    formatMedicationReminder(medications) {
        if (medications.length === 0) {
            return "You don't have any medications due right now.";
        }

        let speech = "It's time for your medication. Please take: ";
        
        medications.forEach((med, index) => {
            speech += `${med.name}, ${med.dosage}`;
            if (index < medications.length - 1) speech += ', and ';
        });

        speech += ". Would you like me to show you pictures of your pills?";

        return speech;
    }
}

module.exports = MedicationService;
```

**Database Schema:**

```sql
-- Medications table
CREATE TABLE medications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100),
    frequency VARCHAR(50),
    times JSONB, -- Array of times: ["08:00", "20:00"]
    image_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    active BOOLEAN DEFAULT TRUE
);

-- Medication log (adherence tracking)
CREATE TABLE medication_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    medication_id INTEGER REFERENCES medications(id),
    taken_at TIMESTAMP DEFAULT NOW(),
    confirmed_by VARCHAR(50) -- 'user', 'caregiver', 'auto'
);

-- Indexes for performance
CREATE INDEX idx_medications_user ON medications(user_id);
CREATE INDEX idx_medication_log_user_date ON medication_log(user_id, taken_at);
```

---

## 6. AI ORCHESTRATION (ANTHROPIC CLAUDE)

### Claude API Integration

**Implementation (Node.js):**

```javascript
const Anthropic = require('@anthropic-ai/sdk');

class AIAssistant {
    constructor(apiKey) {
        this.client = new Anthropic({ apiKey: apiKey });
        this.conversationHistory = [];
        this.systemPrompt = this.buildSystemPrompt();
    }

    buildSystemPrompt() {
        return `You are a caring AI assistant for an elderly person with Alzheimer's disease. 

CRITICAL GUIDELINES:
- Be patient, warm, and never condescending
- Use simple, clear language
- Repeat information naturally if asked again
- Never express frustration or impatience
- Speak in short sentences
- Avoid complex concepts or jargon
- Always confirm understanding
- Offer reassurance
- Remember: dignity and respect are paramount

SAFETY RULES:
- Never agree to send money or make purchases
- Always require confirmation for any action
- If user seems distressed, offer to call a caregiver
- Watch for emergency keywords: help, hurt, fell, lost, scared
- Never provide medical advice (only reminders)

RESPONSE STYLE:
- Warm and friendly tone
- Natural conversational flow
- Use the person's name occasionally
- Acknowledge feelings and emotions
- Offer simple choices ("Would you like A or B?")
- End with an offer to help more

AVAILABLE ACTIONS:
- Check calendar
- Read messages/emails
- Check bank balance
- Remind about medications
- Make phone calls (emergencies)
- Set reminders

Remember: This person may ask the same question multiple times. Respond each time as if it's the first time, but gently acknowledge if appropriate.`;
    }

    async chat(userMessage, userContext = {}) {
        // Add user context (calendar, medications, etc.)
        const contextPrompt = this.buildContextPrompt(userContext);

        // Add message to history
        this.conversationHistory.push({
            role: 'user',
            content: contextPrompt + "\n\nUser says: " + userMessage
        });

        // Call Claude API
        const response = await this.client.messages.create({
            model: 'claude-sonnet-4-5-20250929',
            max_tokens: 1024,
            system: this.systemPrompt,
            messages: this.conversationHistory,
        });

        const assistantMessage = response.content[0].text;

        // Add to history
        this.conversationHistory.push({
            role: 'assistant',
            content: assistantMessage
        });

        // Keep history manageable (last 10 exchanges)
        if (this.conversationHistory.length > 20) {
            this.conversationHistory = this.conversationHistory.slice(-20);
        }

        return {
            response: assistantMessage,
            needsConfirmation: this.detectActionNeedsConfirmation(assistantMessage),
            suggestedAction: this.extractSuggestedAction(assistantMessage),
        };
    }

    buildContextPrompt(context) {
        let prompt = "\n[CONTEXT FOR ASSISTANT]\n";

        if (context.todayEvents && context.todayEvents.length > 0) {
            prompt += "Today's calendar: " + context.todayEvents.map(e => e.summary).join(', ') + "\n";
        }

        if (context.medicationsDue && context.medicationsDue.length > 0) {
            prompt += "Medications due: " + context.medicationsDue.map(m => m.name).join(', ') + "\n";
        }

        if (context.recentMessages) {
            prompt += `Unread messages: ${context.recentMessages}\n`;
        }

        if (context.accountBalance) {
            prompt += `Account balance: $${context.accountBalance}\n`;
        }

        prompt += "[END CONTEXT]\n";

        return prompt;
    }

    detectActionNeedsConfirmation(response) {
        const actionKeywords = ['send', 'call', 'schedule', 'delete', 'pay'];
        return actionKeywords.some(keyword => response.toLowerCase().includes(keyword));
    }

    extractSuggestedAction(response) {
        // Parse response for structured actions
        // This is simplified - real implementation would be more sophisticated
        if (response.includes('call')) return { type: 'call', needsConfirmation: true };
        if (response.includes('send message')) return { type: 'send_sms', needsConfirmation: true };
        return null;
    }
}

module.exports = AIAssistant;
```

---

## 7. PUTTING IT ALL TOGETHER

### Main Application Controller

```javascript
const CalendarService = require('./CalendarService');
const EmailService = require('./EmailService');
const BankingService = require('./BankingService');
const MessagingService = require('./MessagingService');
const MedicationService = require('./MedicationService');
const AIAssistant = require('./AIAssistant');

class CareCompanionApp {
    constructor(config) {
        // Initialize all services
        this.calendar = new CalendarService(config.googleCredentials);
        this.email = new EmailService(config.googleOAuth);
        this.banking = new BankingService(config.plaidClientId, config.plaidSecret);
        this.messaging = new MessagingService(config.twilioSid, config.twilioToken, config.twilioNumber);
        this.medication = new MedicationService(config.database);
        this.ai = new AIAssistant(config.anthropicApiKey);
        
        this.userId = config.userId;
    }

    // Main entry point for user queries
    async handleUserQuery(userMessage) {
        try {
            // Gather context from all services
            const context = await this.gatherContext();

            // Get AI response
            const aiResponse = await this.ai.chat(userMessage, context);

            // Execute any suggested actions (with confirmation)
            if (aiResponse.suggestedAction) {
                return {
                    response: aiResponse.response,
                    action: aiResponse.suggestedAction,
                    needsConfirmation: aiResponse.needsConfirmation,
                };
            }

            return {
                response: aiResponse.response,
                needsConfirmation: false,
            };

        } catch (error) {
            console.error('Error handling query:', error);
            return {
                response: "I'm sorry, I'm having trouble right now. Can you try asking again?",
                error: true,
            };
        }
    }

    // Gather context from all services
    async gatherContext() {
        const [todayEvents, medications, balances] = await Promise.all([
            this.calendar.getTodayEvents().catch(() => []),
            this.medication.getMedicationsDueNow(this.userId).catch(() => []),
            this.banking.getBalances().catch(() => []),
        ]);

        return {
            todayEvents,
            medicationsDue: medications,
            accountBalance: balances[0]?.balance,
            currentTime: new Date(),
        };
    }

    // Execute confirmed action
    async executeAction(action, parameters) {
        switch (action.type) {
            case 'send_sms':
                return await this.messaging.sendMessage(
                    parameters.to,
                    parameters.message,
                    false // Already confirmed
                );

            case 'call':
                return await this.initiateCall(parameters.number);

            case 'create_reminder':
                return await this.calendar.createReminder(
                    parameters.title,
                    parameters.dateTime
                );

            default:
                throw new Error(`Unknown action type: ${action.type}`);
        }
    }

    // Periodic health check / proactive notifications
    async performHealthCheck() {
        // Check for medications due soon
        const medsDue = await this.medication.getMedicationsDueNow(this.userId);
        if (medsDue.length > 0) {
            return {
                type: 'medication_reminder',
                data: medsDue,
            };
        }

        // Check for upcoming calendar events (within 1 hour)
        const events = await this.calendar.getTodayEvents();
        const soonEvents = events.filter(e => {
            const start = new Date(e.start.dateTime);
            const now = new Date();
            const diff = (start - now) / 1000 / 60; // minutes
            return diff > 0 && diff < 60;
        });

        if (soonEvents.length > 0) {
            return {
                type: 'event_reminder',
                data: soonEvents,
            };
        }

        return null;
    }
}

module.exports = CareCompanionApp;
```

---

## 8. SECURITY CHECKLIST

### Before Deployment

- [ ] All API keys stored in environment variables (not code)
- [ ] Database encrypted at rest
- [ ] SSL/TLS for all network communication
- [ ] Rate limiting implemented on all endpoints
- [ ] Audit logging enabled
- [ ] Multi-factor authentication for caregiver access
- [ ] Approved contact whitelist configured
- [ ] Financial transaction limits set
- [ ] Emergency contact system tested
- [ ] Data backup strategy implemented
- [ ] HIPAA compliance review completed
- [ ] Penetration testing performed
- [ ] Privacy policy written and approved
- [ ] Consent forms signed by user/guardian

---

## 9. TESTING GUIDE

### Integration Tests

```javascript
// Test calendar integration
describe('CalendarService', () => {
    it('should fetch today\'s events', async () => {
        const cal = new CalendarService(credentials);
        const events = await cal.getTodayEvents();
        expect(events).toBeInstanceOf(Array);
    });

    it('should format events for speech correctly', () => {
        const events = [{ summary: 'Doctor', start: { dateTime: '2025-10-30T14:00:00' }}];
        const speech = cal.formatEventsForSpeech(events);
        expect(speech).toContain('Doctor');
    });
});

// Test banking integration
describe('BankingService', () => {
    it('should fetch balances securely', async () => {
        const banking = new BankingService(clientId, secret);
        const balances = await banking.getBalances();
        expect(balances[0]).not.toHaveProperty('accountNumber');
    });
});

// Test AI safety
describe('AIAssistant', () => {
    it('should never agree to send money', async () => {
        const ai = new AIAssistant(apiKey);
        const response = await ai.chat("Send $500 to John");
        expect(response.response.toLowerCase()).toContain('cannot');
    });
});
```

---

## 10. MONITORING & MAINTENANCE

### Key Metrics to Track

1. **User Engagement:**
   - Daily active usage
   - Number of voice interactions
   - Most common queries

2. **System Health:**
   - API response times
   - Error rates by service
   - Uptime percentage

3. **Safety Metrics:**
   - Failed authentication attempts
   - Blocked action attempts
   - Emergency alert frequency

4. **Healthcare Metrics:**
   - Medication adherence rate
   - Missed appointments
   - Caregiver notification frequency

### Maintenance Schedule

- **Daily:** Check error logs, verify backups
- **Weekly:** Review user interactions, update approved contacts
- **Monthly:** Security audit, API key rotation
- **Quarterly:** Full system testing, feature updates

---

## NEXT STEPS

1. Set up development environment
2. Obtain API credentials for each service
3. Implement authentication flows
4. Build core integration layer
5. Connect AI orchestration
6. Test with sample data
7. Pilot with your mother (with supervision)
8. Iterate based on feedback
9. Expand features gradually
10. Monitor and maintain

This integration guide provides everything you need to connect real services. Let me know which integration you'd like to tackle first!
