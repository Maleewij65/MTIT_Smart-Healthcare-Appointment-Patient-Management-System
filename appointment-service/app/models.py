from pydantic import BaseModel, Field
from typing import Optional

# ── Request model — Create ─────────────────────────────
class AppointmentCreate(BaseModel):
    patient_id: str = Field(..., example="p001", description="ID of the patient")
    doctor_id: str = Field(..., example="d001", description="ID of the doctor")
    appointment_date: str = Field(..., example="2026-04-10", description="Date YYYY-MM-DD")
    appointment_time: str = Field(..., example="10:30", description="Time HH:MM")
    reason: str = Field(..., example="Routine check-up", description="Reason for visit")
    status: Optional[str] = Field("scheduled", example="scheduled",
                                   description="scheduled | completed | cancelled")

# ── Request model — Update ─────────────────────────────
class AppointmentUpdate(BaseModel):
    patient_id: Optional[str] = Field(None, example="p001")
    doctor_id: Optional[str] = Field(None, example="d001")
    appointment_date: Optional[str] = Field(None, example="2026-04-15")
    appointment_time: Optional[str] = Field(None, example="11:00")
    reason: Optional[str] = Field(None, example="Follow-up visit")
    status: Optional[str] = Field(None, example="completed",
                                   description="scheduled | completed | cancelled")
