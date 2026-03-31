from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Request Model (Input)
class Patient(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=0, lt=120)
    gender: str = Field(..., min_length=3, max_length=10)
    contact: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    medicalHistory: Optional[str] = None


# Response Model (Output)
class PatientResponse(Patient):
    id: str