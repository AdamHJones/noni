from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Medication(Base):
    """Medication model for tracking prescriptions"""

    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String)
    frequency = Column(String)  # 'daily', 'twice_daily', 'weekly', etc.
    times = Column(JSON)  # List of times: ["08:00", "20:00"]
    image_url = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to medication logs
    logs = relationship("MedicationLog", back_populates="medication")


class MedicationLog(Base):
    """Log of when medications were taken"""

    __tablename__ = "medication_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    taken_at = Column(DateTime, default=datetime.utcnow, index=True)
    confirmed_by = Column(String)  # 'user', 'caregiver', 'auto'
    notes = Column(String, nullable=True)

    # Relationship back to medication
    medication = relationship("Medication", back_populates="logs")


class User(Base):
    """User model for the patient"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String, nullable=True)
    timezone = Column(String, default="America/Denver")

    # External service tokens (encrypted in real app)
    google_access_token = Column(String, nullable=True)
    google_refresh_token = Column(String, nullable=True)
    plaid_access_token = Column(String, nullable=True)

    # Caregiver info
    caregiver_email = Column(String, nullable=True)
    caregiver_phone = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ApprovedContact(Base):
    """Whitelist of approved contacts for communication"""

    __tablename__ = "approved_contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    relationship = Column(String)  # 'daughter', 'son', 'caregiver', etc.
    photo_url = Column(String, nullable=True)
    can_receive_messages = Column(Boolean, default=True)
    can_receive_calls = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
