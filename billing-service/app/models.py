from pydantic import BaseModel
from typing import Optional


# -------------------------------
# CREATE MODEL
# -------------------------------
class BillCreate(BaseModel):
    patient_id: str
    appointment_id: str
    doctor_id: str
    description: str
    amount: float
    payment_method: str = "cash"
    payment_status: str = "pending"


# -------------------------------
# UPDATE MODEL
# -------------------------------
class BillUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None


# -------------------------------
# RESPONSE MODEL
# -------------------------------
class BillResponse(BaseModel):
    id: str
    patient_id: str
    appointment_id: str
    doctor_id: str
    description: str
    amount: float
    payment_method: str
    payment_status: str