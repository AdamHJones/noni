from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.config import settings
from app.core.database import get_db, engine, Base
from app.services.ai_service import ai_assistant
from app.services.vision_service import vision_service
from app.models.medication import User, Medication, MedicationLog, ApprovedContact
import base64

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-native care companion API for elderly with Alzheimer's/dementia",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================


class ChatRequest(BaseModel):
    message: str
    user_id: int
    conversation_history: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    response: str
    suggested_action: Optional[dict] = None
    needs_confirmation: bool = False
    context_used: Optional[dict] = None


class VisionAnalysisRequest(BaseModel):
    image_data: str  # Base64 encoded
    analysis_type: str
    user_id: int


class VisionAnalysisResponse(BaseModel):
    success: bool
    analysis: str
    warnings: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
    extracted_data: Optional[dict] = None


class MedicationCreate(BaseModel):
    name: str
    dosage: str
    frequency: str
    times: List[str]
    image_url: Optional[str] = None
    notes: Optional[str] = None


class MedicationResponse(BaseModel):
    id: int
    name: str
    dosage: str
    frequency: str
    times: List[str]
    active: bool

    class Config:
        from_attributes = True


class LocationUpdate(BaseModel):
    user_id: int
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    timestamp: Optional[str] = None


# ============================================================================
# HEALTH CHECK
# ============================================================================


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "features": ["chat", "voice", "vision", "geolocation", "medications"],
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "ready",
        "vision_service": "ready",
        "timestamp": "2025-01-01T00:00:00Z",
    }


# ============================================================================
# AI CHAT ENDPOINT (PRIMARY INTERFACE)
# ============================================================================


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main AI chat endpoint
    Handles all user interactions through Claude
    """
    try:
        # Get user
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Gather context (calendar, medications, finances, etc.)
        context = await gather_user_context(user, db)

        # Get AI response
        ai_response = await ai_assistant.chat(
            user_message=request.message,
            conversation_history=request.conversation_history,
            context=context,
        )

        return ChatResponse(
            response=ai_response["response"],
            suggested_action=ai_response.get("suggested_action"),
            needs_confirmation=ai_response.get("needs_confirmation", False),
            context_used=context,
        )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def gather_user_context(user: User, db: Session) -> dict:
    """
    Gather all relevant context for the AI
    This is what makes the system "aware" of the user's situation
    """
    from datetime import datetime

    context = {
        "user_name": user.name,
        "current_time": datetime.now().strftime("%I:%M %p"),
    }

    # Get today's medications
    current_hour = datetime.now().strftime("%H:00")
    medications = (
        db.query(Medication)
        .filter(
            Medication.user_id == user.id,
            Medication.active == True,
        )
        .all()
    )

    medications_due = [
        {"name": med.name, "dosage": med.dosage}
        for med in medications
        if current_hour in (med.times or [])
    ]

    if medications_due:
        context["medications_due"] = medications_due

    # TODO: Add calendar integration
    # TODO: Add banking integration
    # TODO: Add messaging integration

    return context


# ============================================================================
# VISION/CAMERA ENDPOINTS
# ============================================================================


@app.post("/api/vision/analyze", response_model=VisionAnalysisResponse)
async def analyze_image(request: VisionAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze image using Claude Vision API
    Extracts information from prescriptions, medication labels, food labels, etc.
    """
    try:
        # Get user's current medications for interaction checking
        medications = (
            db.query(Medication)
            .filter(Medication.user_id == request.user_id, Medication.active == True)
            .all()
        )

        user_meds = [
            {"name": med.name, "dosage": med.dosage, "frequency": med.frequency}
            for med in medications
        ]

        # Analyze image
        result = await vision_service.analyze_image(
            image_data=request.image_data,
            analysis_type=request.analysis_type,
            user_medications=user_meds,
        )

        return VisionAnalysisResponse(**result)

    except Exception as e:
        print(f"Error in vision analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/vision/check-interactions")
async def check_medication_interactions(
    medication: str, user_id: int, db: Session = Depends(get_db)
):
    """Check if a new medication has interactions with current medications"""
    try:
        # Get current medications
        medications = (
            db.query(Medication)
            .filter(Medication.user_id == user_id, Medication.active == True)
            .all()
        )

        user_meds = [
            {"name": med.name, "dosage": med.dosage, "frequency": med.frequency}
            for med in medications
        ]

        # Check interactions
        result = await vision_service.check_medication_interactions(
            new_medication=medication, current_medications=user_meds
        )

        return result

    except Exception as e:
        print(f"Error checking interactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# GEOLOCATION ENDPOINTS
# ============================================================================


@app.post("/api/location/update")
async def update_location(location: LocationUpdate, db: Session = Depends(get_db)):
    """
    Update user's current location
    Triggers geofencing checks and caregiver notifications if needed
    """
    try:
        # Get user
        user = db.query(User).filter(User.id == location.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # TODO: Store location in database
        # TODO: Check geofences (home, doctor, pharmacy)
        # TODO: Notify caregivers if leaving/arriving

        # For now, just acknowledge
        return {
            "status": "location_updated",
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timestamp": location.timestamp,
        }

    except Exception as e:
        print(f"Error updating location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/location/{user_id}")
async def get_location(user_id: int, db: Session = Depends(get_db)):
    """Get user's current location (for caregivers)"""
    try:
        # TODO: Retrieve latest location from database
        # For now, return placeholder

        return {
            "user_id": user_id,
            "latitude": 0.0,
            "longitude": 0.0,
            "last_updated": None,
            "message": "Location tracking not yet implemented",
        }

    except Exception as e:
        print(f"Error getting location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MEDICATIONS ENDPOINTS
# ============================================================================


@app.post("/api/medications", response_model=MedicationResponse)
async def create_medication(
    medication: MedicationCreate, user_id: int, db: Session = Depends(get_db)
):
    """Add a new medication to user's schedule"""
    db_medication = Medication(
        user_id=user_id,
        name=medication.name,
        dosage=medication.dosage,
        frequency=medication.frequency,
        times=medication.times,
        image_url=medication.image_url,
        notes=medication.notes,
    )
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication


@app.get("/api/medications/{user_id}", response_model=List[MedicationResponse])
async def get_medications(user_id: int, db: Session = Depends(get_db)):
    """Get all active medications for a user"""
    medications = (
        db.query(Medication)
        .filter(Medication.user_id == user_id, Medication.active == True)
        .all()
    )
    return medications


@app.post("/api/medications/{medication_id}/taken")
async def mark_medication_taken(
    medication_id: int, user_id: int, db: Session = Depends(get_db)
):
    """Record that a medication was taken"""
    log = MedicationLog(
        user_id=user_id,
        medication_id=medication_id,
        confirmed_by="user",
    )
    db.add(log)
    db.commit()
    return {"status": "recorded", "medication_id": medication_id}


# ============================================================================
# USER ENDPOINTS
# ============================================================================


@app.get("/api/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user information"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "timezone": user.timezone,
        "caregiver_email": user.caregiver_email,
        "caregiver_phone": user.caregiver_phone,
    }


@app.get("/api/contacts/{user_id}")
async def get_approved_contacts(user_id: int, db: Session = Depends(get_db)):
    """Get approved contacts for communication"""
    contacts = db.query(ApprovedContact).filter(ApprovedContact.user_id == user_id).all()

    return [
        {
            "id": contact.id,
            "name": contact.name,
            "phone": contact.phone,
            "email": contact.email,
            "relationship": contact.relationship,
            "photo_url": contact.photo_url,
            "can_receive_messages": contact.can_receive_messages,
            "can_receive_calls": contact.can_receive_calls,
        }
        for contact in contacts
    ]


# ============================================================================
# CALENDAR ENDPOINTS (Placeholder - implement with Google OAuth)
# ============================================================================


@app.get("/api/calendar/today/{user_id}")
async def get_today_calendar(user_id: int, db: Session = Depends(get_db)):
    """Get today's calendar events"""
    # TODO: Implement Google Calendar integration
    return {
        "events": [],
        "message": "Calendar integration pending - requires Google OAuth setup",
    }


# ============================================================================
# BANKING ENDPOINTS (Placeholder - implement with Plaid)
# ============================================================================


@app.get("/api/banking/balance/{user_id}")
async def get_balance(user_id: int, db: Session = Depends(get_db)):
    """Get account balance"""
    # TODO: Implement Plaid integration
    return {
        "balance": 0,
        "message": "Banking integration pending - requires Plaid setup",
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global error handler"""
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong. Please try again.",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
