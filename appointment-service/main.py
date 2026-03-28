from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import uvicorn

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Appointment Service",
    description="Smart Healthcare – Appointment & Patient Management System",
    version="1.0.0",
)

# ── MongoDB connection ──────────────────────────────────────────────────────────
MONGO_URI = "mongodb+srv://Hospital_MTIT:hospital123@cluster0.lnhqemi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["healthcare_db"]
appointments_col = db["appointments"]

# ── Helper ─────────────────────────────────────────────────────────────────────
def str_to_objectid(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {id}")

def serialize(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict."""
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# ── Pydantic models ────────────────────────────────────────────────────────────
class AppointmentCreate(BaseModel):
    patient_id: str = Field(..., example="p001", description="ID of the patient")
    doctor_id: str = Field(..., example="d001", description="ID of the doctor")
    appointment_date: str = Field(..., example="2026-04-10", description="Date (YYYY-MM-DD)")
    appointment_time: str = Field(..., example="10:30", description="Time (HH:MM)")
    reason: str = Field(..., example="Routine check-up", description="Reason for visit")
    status: Optional[str] = Field("scheduled", example="scheduled",
                                   description="scheduled | completed | cancelled")

class AppointmentUpdate(BaseModel):
    patient_id: Optional[str] = Field(None, example="p001")
    doctor_id: Optional[str] = Field(None, example="d001")
    appointment_date: Optional[str] = Field(None, example="2026-04-15")
    appointment_time: Optional[str] = Field(None, example="11:00")
    reason: Optional[str] = Field(None, example="Follow-up visit")
    status: Optional[str] = Field(None, example="completed",
                                   description="scheduled | completed | cancelled")

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"service": "Appointment Service", "status": "running", "port": 8003}


# --- CREATE ---
@app.post("/appointments", tags=["Appointments"], status_code=201)
def create_appointment(data: AppointmentCreate):
    """Book a new appointment."""
    doc = data.dict()
    doc["created_at"] = datetime.utcnow().isoformat()
    result = appointments_col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return {"message": "Appointment created successfully", "appointment": doc}


# --- READ ALL ---
@app.get("/appointments", tags=["Appointments"])
def get_all_appointments():
    """List all appointments."""
    appointments = [serialize(doc) for doc in appointments_col.find()]
    return {"total": len(appointments), "appointments": appointments}


# --- READ ONE ---
@app.get("/appointments/{appointment_id}", tags=["Appointments"])
def get_appointment(appointment_id: str):
    """Get a single appointment by ID."""
    doc = appointments_col.find_one({"_id": str_to_objectid(appointment_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return serialize(doc)


# --- READ BY PATIENT ---
@app.get("/appointments/patient/{patient_id}", tags=["Appointments"])
def get_appointments_by_patient(patient_id: str):
    """Get all appointments for a specific patient."""
    docs = [serialize(doc) for doc in appointments_col.find({"patient_id": patient_id})]
    if not docs:
        raise HTTPException(status_code=404, detail="No appointments found for this patient")
    return {"patient_id": patient_id, "total": len(docs), "appointments": docs}


# --- READ BY DOCTOR ---
@app.get("/appointments/doctor/{doctor_id}", tags=["Appointments"])
def get_appointments_by_doctor(doctor_id: str):
    """Get all appointments for a specific doctor."""
    docs = [serialize(doc) for doc in appointments_col.find({"doctor_id": doctor_id})]
    if not docs:
        raise HTTPException(status_code=404, detail="No appointments found for this doctor")
    return {"doctor_id": doctor_id, "total": len(docs), "appointments": docs}


# --- UPDATE ---
@app.put("/appointments/{appointment_id}", tags=["Appointments"])
def update_appointment(appointment_id: str, data: AppointmentUpdate):
    """Reschedule or update an appointment."""
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    update_data["updated_at"] = datetime.utcnow().isoformat()
    result = appointments_col.update_one(
        {"_id": str_to_objectid(appointment_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")

    updated = appointments_col.find_one({"_id": str_to_objectid(appointment_id)})
    return {"message": "Appointment updated successfully", "appointment": serialize(updated)}


# --- DELETE ---
@app.delete("/appointments/{appointment_id}", tags=["Appointments"])
def delete_appointment(appointment_id: str):
    """Cancel and delete an appointment."""
    result = appointments_col.delete_one({"_id": str_to_objectid(appointment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted successfully", "id": appointment_id}


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
