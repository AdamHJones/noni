# Vision & Location Features - Care Companion

## Overview

The Care Companion app now includes powerful camera vision and geolocation capabilities to help your mother navigate daily life more safely and independently.

---

## Camera Vision Features

### What It Does

The app can analyze photos of everyday items using Claude's Vision API to extract important information and check for potential issues.

### 7 Analysis Types

#### 1. Prescription (💊)
**Use Case**: Take a photo of a prescription from the doctor

**What It Extracts**:
- Medication name and dosage
- How often to take it
- Duration of treatment
- Doctor's name
- Pharmacy instructions

**Safety Check**: Automatically checks for interactions with current medications

**Example**: "Take photo of new prescription from Dr. Smith" → Shows if it's safe to take with her other medications

---

#### 2. Medication Label (🏷️)
**Use Case**: Read the label on a medication bottle

**What It Extracts**:
- Drug name (generic and brand)
- Dosage strength
- Expiration date
- Storage instructions
- Warning labels

**Safety Check**: Compares against current medication list for duplicates or interactions

**Example**: "Is this the right pill?" → Confirms identity and checks expiration

---

#### 3. Doctor Note (📋)
**Use Case**: Understand written instructions from appointments

**What It Extracts**:
- Diagnosis summary
- Treatment instructions
- Follow-up appointments
- Lab test results
- Dietary restrictions

**Safety Check**: Flags any new medications or contraindications

**Example**: "What did the doctor say?" → Summarizes notes in simple language

---

#### 4. Recipe (🍳)
**Use Case**: Follow cooking instructions

**What It Extracts**:
- Ingredient list
- Step-by-step directions (simplified)
- Cooking time and temperature
- Serving size

**Safety Check**: Checks ingredients against dietary restrictions and medication interactions (e.g., grapefruit with certain drugs)

**Example**: "Can I make this recipe?" → Confirms it's safe with her medications and diet

---

#### 5. Food Label (🥫)
**Use Case**: Check what's in packaged food

**What It Extracts**:
- Main ingredients
- Allergen warnings
- Expiration date
- Serving information

**Safety Check**: Flags allergens, dietary restrictions, and food-drug interactions

**Example**: "What's in this can?" → Reads label and confirms it's safe

---

#### 6. Nutrition Info (📊)
**Use Case**: Understand nutritional content

**What It Extracts**:
- Calories per serving
- Key nutrients (sodium, sugar, protein)
- Health warnings (e.g., high sodium)

**Safety Check**: Compares against dietary restrictions (low-sodium, diabetic-friendly, etc.)

**Example**: "Is this healthy for me?" → Checks against her health conditions

---

#### 7. Sign/Small Text (🔤)
**Use Case**: Read signs, labels, or text that's too small

**What It Extracts**:
- All visible text
- Simplified explanation
- Key information highlighted

**Safety Check**: N/A (informational only)

**Example**: "What does this sign say?" → Reads and explains in large text with voice

---

## How It Works

### Step-by-Step Process

1. **User taps "Scan Photo" button** on main screen
2. **Selects analysis type** (prescription, medication, etc.)
3. **Takes photo** using iPhone camera or selects from gallery
4. **Image sent to Claude Vision API** for analysis
5. **Results displayed** within 2-5 seconds:
   - Extracted information in large, readable text
   - Safety warnings (if any) in red
   - Suggestions in green
   - Voice reads results aloud automatically

### Medication Interaction Checking

**How It Protects Her**:
- Every medication-related scan is checked against her current medication list
- Claude analyzes potential drug-drug interactions
- Warns about:
  - Duplicate medications
  - Dangerous combinations
  - Food-drug interactions
  - Timing issues (take with/without food)

**Example Scenario**:
```
User scans new prescription for blood thinner

Analysis shows:
✓ Medication: Warfarin 5mg
⚠️ WARNING: This may interact with your current aspirin
⚠️ WARNING: Avoid grapefruit, green leafy vegetables
💡 SUGGESTION: Consult pharmacist before starting
💡 SUGGESTION: Notify caregiver Sarah

App automatically sends alert to caregiver
```

---

## Geolocation Features

### What It Does

The app can track your mother's location and notify caregivers when she arrives or leaves important places.

### Key Capabilities

#### Real-Time Location Tracking

**How It Works**:
- User taps "Share Location" button to turn on tracking
- App continuously monitors GPS location
- Updates caregiver dashboard every 1-5 minutes (configurable)
- Works in background (if app is open)

**Privacy**:
- User must explicitly turn on tracking
- Clear indicator when tracking is active
- Can be turned off anytime
- Location data encrypted

**Battery Optimization**:
- Uses "significant change" monitoring (not continuous GPS)
- Only updates when location changes by 100+ meters
- Can be set to "high accuracy" for safety situations

---

#### Geofencing (Arrival/Departure Notifications)

**What It Does**: Set up virtual boundaries around important locations

**Example Locations**:
- Home
- Doctor's office
- Grocery store
- Sarah's house (daughter)
- Senior center
- Church

**How Caregivers Use It**:

1. **Set Up Geofences** (one-time):
   - Add location name and address
   - Set radius (e.g., 100 meters around home)
   - Choose notification preferences

2. **Receive Alerts**:
   - "Mom arrived at doctor's office at 2:15 PM"
   - "Mom left home at 10:30 AM" (unexpected departure alert)
   - "Mom has been at grocery store for 45 minutes" (time-based alert)

**Safety Scenarios**:

**Scenario 1: Wandering Prevention**
```
Mom leaves home at 11 PM (unusual time)
→ Immediate alert to caregiver
→ "Your mother left home at 11:03 PM. Last known location: 123 Main St heading north."
→ Caregiver can call or go check on her
```

**Scenario 2: Appointment Confirmation**
```
Mom arrives at doctor's office
→ Caregiver receives notification
→ "Your mother arrived at Dr. Smith's office at 2:10 PM."
→ Caregiver knows she made it safely
```

**Scenario 3: Lost/Confused**
```
Mom calls: "I don't know where I am"
→ Caregiver opens app, sees exact location on map
→ Can provide directions or send help
```

---

### Caregiver Dashboard Features

**Location View**:
- Real-time map showing current location
- Location history (last 24 hours)
- Geofence boundaries visualized
- Battery level of phone

**Notifications**:
- Arrival/departure alerts
- Unusual time alerts (e.g., leaving home at night)
- Low battery warnings
- "Check in" reminders if no movement detected

**Safety Features**:
- One-tap emergency call
- Send current location to 911
- Share location with family members
- "Find my phone" if lost

---

## Technical Implementation

### Backend API Endpoints

**Vision Analysis**:
```
POST /api/vision/analyze
Body: {
  "image_data": "base64_encoded_image",
  "analysis_type": "prescription|medication|doctor_note|recipe|food_label|nutrition|sign",
  "user_id": 1
}

Response: {
  "analysis": "Extracted information in simple language",
  "warnings": ["Drug interaction warnings"],
  "suggestions": ["Recommended actions"],
  "raw_data": {"medication": "...", "dosage": "..."}
}
```

**Location Updates**:
```
POST /api/location/update
Body: {
  "user_id": 1,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "accuracy": 10,
  "timestamp": "2025-01-15T14:30:00Z"
}

GET /api/location/{user_id}
Response: {
  "latitude": 37.7749,
  "longitude": -122.4194,
  "last_updated": "2025-01-15T14:30:00Z",
  "address": "123 Main St, San Francisco, CA"
}
```

### Frontend Components

**CameraCapture.tsx**:
- Handles photo capture and selection
- 7 analysis type buttons with icons
- Preview before sending
- Loading state during analysis

**PhotoAnalysis.tsx**:
- Displays results in color-coded sections
- Voice reads results aloud
- Save to history button
- Share with caregiver button

**LocationTracker.tsx**:
- On/off toggle for tracking
- Current location display
- Accuracy indicator
- Battery usage estimate

---

## Privacy & Security

### Data Protection

**Images**:
- Never stored on servers (processed in memory only)
- Sent to Claude API via encrypted connection
- Anthropic does not train on your data
- Can be saved locally if user chooses (encrypted)

**Location Data**:
- Encrypted in transit (HTTPS)
- Encrypted at rest (AES-256)
- Only accessible to authorized caregivers
- Can be deleted anytime
- 30-day automatic deletion of historical data

### HIPAA Compliance

- Business Associate Agreement with Anthropic (required for production)
- All PHI encrypted
- Access logging (who viewed what, when)
- Breach notification procedures in place

---

## Cost Breakdown

### Vision Analysis

**Claude Vision API Pricing**:
- $0.048 per image (with text extraction)
- Average use: 5-10 photos/day = $0.24-$0.48/day
- **Monthly cost: $7-15**

**Cost Optimization**:
- Cache common medications (reduces API calls)
- Batch processing if multiple photos
- Use lower-cost model for simple text extraction

### Geolocation

**Free** (uses browser Geolocation API)
- No API costs
- No third-party services required
- Battery usage: ~2-5% per day

**Estimated Total Additional Cost: $7-15/month**

---

## Setup Instructions

### 1. Enable Camera Permissions (iPhone)

**First Time Use**:
1. Tap "Scan Photo" button
2. iPhone will ask "Allow Care Companion to access camera?"
3. Tap "Allow"

**If Previously Denied**:
1. Open iPhone Settings
2. Scroll to "Care Companion" app
3. Tap "Camera" → Select "Allow"

### 2. Enable Location Permissions

**First Time Use**:
1. Tap "Share Location" button
2. iPhone will ask "Allow Care Companion to access location?"
3. Choose "Allow While Using App" or "Always Allow" (recommended)

**If Previously Denied**:
1. Open iPhone Settings
2. Scroll to "Care Companion" app
3. Tap "Location" → Select "Always" (best for safety)

### 3. Configure Medication List (Important!)

**Why**: For accurate interaction checking

**How**:
1. Caregiver logs into dashboard
2. Go to "Medications" section
3. Add all current medications:
   - Name
   - Dosage
   - Frequency
   - Prescribing doctor
4. Update whenever medications change

### 4. Set Up Geofences (Optional but Recommended)

**For Caregivers**:
1. Open caregiver dashboard
2. Click "Geofences" tab
3. Add important locations:
   - Name: "Home"
   - Address: "123 Main St..."
   - Radius: 100 meters
   - Notifications: "Alert on departure"
4. Save

**Recommended Geofences**:
- Home (alert on night departures)
- Pharmacy (confirm pickup)
- Doctor's offices (confirm arrivals)
- Grocery store (time-based alerts if too long)
- Family members' homes

---

## Testing the Features

### Test Camera Vision

**Test 1: Medication Label**
1. Find a medication bottle
2. Tap "Scan Photo"
3. Select "Medication Label"
4. Take clear photo of label
5. Wait 3-5 seconds
6. Review results

**Expected Results**:
- Medication name displayed in large text
- Dosage and instructions shown
- Expiration date highlighted
- Voice reads information aloud

**Test 2: Food Label**
1. Find packaged food
2. Select "Food Label" analysis type
3. Take photo of ingredients list
4. Review safety warnings

### Test Location Tracking

**Test 1: Basic Tracking**
1. Tap "Share Location" button
2. Wait for "Tracking Active" status
3. Walk around block
4. Caregiver checks dashboard to see location updates

**Test 2: Geofence**
1. Set up geofence around current location (100m radius)
2. Walk outside the boundary
3. Caregiver should receive departure notification
4. Walk back inside boundary
5. Caregiver should receive arrival notification

---

## Troubleshooting

### Camera Issues

**"Camera not working"**
- Check permissions in iPhone Settings
- Restart app
- Restart iPhone
- Ensure app is updated

**"Poor image quality"**
- Hold phone steady
- Ensure good lighting
- Clean camera lens
- Get closer to label/document

**"Analysis taking too long"**
- Check internet connection
- Image may be too large (reduce size)
- Server may be busy (try again)

### Location Issues

**"Can't get location"**
- Enable Location Services in iPhone Settings
- Ensure app has "Always Allow" permission
- Check if airplane mode is on
- Try moving outside (better GPS signal)

**"Location not updating"**
- Battery saver mode may limit updates
- App must be open for continuous tracking
- Check internet connection for data upload

**"Notifications not received"**
- Check caregiver notification settings
- Ensure email/SMS notifications enabled
- Check spam folder for emails

---

## Use Cases for Your Mother

### Daily Life Scenarios

**Morning Medication**:
1. Voice: "What pills should I take?"
2. App shows medication schedule
3. "Show me my pills" → Takes photo of pill organizer
4. App confirms correct pills for morning

**Grocery Shopping**:
1. Finds interesting item on shelf
2. Takes photo of nutrition label
3. App checks against dietary restrictions
4. "Safe to eat" or "Avoid - high sodium"

**Doctor Visit**:
1. Doctor writes prescription
2. Takes photo before leaving
3. App checks for interactions
4. Alerts caregiver if concerns
5. Can show photo to pharmacist

**Lost/Confused**:
1. "I don't know where I am"
2. App sends location to caregiver
3. Caregiver can provide directions or assistance

**Reading Small Print**:
1. Can't read thermostat, appliance label, etc.
2. Takes photo with "Sign/Text" mode
3. App displays in large text and reads aloud

---

## Privacy Considerations for Families

### What Caregivers Can See

**Always Visible**:
- Current location (if tracking enabled)
- Medication adherence
- Photo analysis history (if saved)
- Activity patterns

**Never Visible**:
- Private messages (unless explicitly shared)
- Photos not saved to history
- Bank account numbers
- Passwords

### Balancing Safety and Dignity

**Transparent Tracking**:
- User knows when tracking is on (clear indicator)
- Can turn off temporarily (caregiver notified)
- Explanation in simple terms: "So Sarah knows you're safe"

**Respectful Notifications**:
- Caregivers can set "quiet hours" (no alerts unless emergency)
- Normal activities don't trigger alerts
- Only unusual patterns notify caregivers

---

## Future Enhancements

### Planned Features

1. **Offline OCR**: Use on-device text recognition when internet unavailable
2. **Voice-Activated Camera**: "Take a photo of this pill bottle"
3. **Automatic Pill Identification**: Match photo to known pills visually
4. **Route Tracking**: Show path taken during walks
5. **Safe Zones**: Alert if leaving familiar area
6. **Fall Detection**: Use accelerometer to detect falls
7. **Integration with Pharmacy**: Auto-refill reminders based on photo analysis

### DeepSeek OCR Integration (Planned)

**Why Add DeepSeek**:
- Specialized in medical/pharmaceutical text
- Higher accuracy for prescription OCR
- Can process handwritten doctor notes better
- Free and open-source (cost savings)

**How It Will Work**:
- Use DeepSeek for initial text extraction
- Use Claude for interpretation and safety checking
- Best of both: accuracy + understanding

---

## Questions?

**For Technical Support**:
- Email: support@carecompanion.app (not yet active)
- GitHub Issues: https://github.com/AdamHJones/noni/issues

**For Medical/Safety Concerns**:
- Always consult healthcare providers
- 911 for emergencies
- App is a tool, not a replacement for professional care

---

**Last Updated**: January 15, 2025
**Version**: 1.0 (MVP with Vision & Location)
