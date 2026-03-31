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
    title="Doctor Service",
    description="Smart Healthcare – Doctor Service for CRUD operations",
    version="1.0.0",
)

# ── MongoDB connection ──────────────────────────────────────────────────────────
MONGO_URI = "mongodb+srv://Hospital_MTIT:hospital123@cluster0.lnhqemi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["healthcare_doctor_db"]
doctors_col = db["doctors"]

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
class DoctorCreate(BaseModel):
    full_name: str = Field(..., example="Dr. Nimal Perera", description="Doctor full name")
    specialization: str = Field(..., example="Cardiology", description="Doctor specialization")
    email: str = Field(..., example="nimal.perera@example.com", description="Contact email")
    phone: str = Field(..., example="0771234567", description="Contact phone number")
    license_number: str = Field(..., example="SLMC-12345", description="Medical license number")
    availability_status: Optional[str] = Field("AVAILABLE", example="AVAILABLE",
                                              description="AVAILABLE | UNAVAILABLE")
    available_from: Optional[str] = Field("09:00", example="09:00", description="Availability start time")
    available_to: Optional[str] = Field("16:00", example="16:00", description="Availability end time")

class DoctorUpdate(BaseModel):
    full_name: Optional[str] = Field(None, example="Dr. Nimal Perera")
    specialization: Optional[str] = Field(None, example="Cardiology")
    email: Optional[str] = Field(None, example="nimal.perera@example.com")
    phone: Optional[str] = Field(None, example="0771234567")
    license_number: Optional[str] = Field(None, example="SLMC-12345")
    availability_status: Optional[str] = Field(None, example="AVAILABLE")
    available_from: Optional[str] = Field(None, example="09:00")
    available_to: Optional[str] = Field(None, example="16:00")

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"service": "Doctor Service", "status": "running", "port": 8002}


# --- CREATE ---
@app.post("/doctors", tags=["Doctors"], status_code=201)
def create_doctor(data: DoctorCreate):
    """Add a new doctor."""
    doc = data.dict()
    doc["created_at"] = datetime.utcnow().isoformat()
    result = doctors_col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return {"message": "Doctor created successfully", "doctor": doc}


# --- READ ALL ---
@app.get("/doctors", tags=["Doctors"])
def get_all_doctors():
    """List all doctors."""
    doctors = [serialize(doc) for doc in doctors_col.find()]
    return {"total": len(doctors), "doctors": doctors}


# --- READ ONE ---
@app.get("/doctors/{doctor_id}", tags=["Doctors"])
def get_doctor(doctor_id: str):
    """Get a single doctor by ID."""
    doc = doctors_col.find_one({"_id": str_to_objectid(doctor_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return serialize(doc)


# --- UPDATE ---
@app.put("/doctors/{doctor_id}", tags=["Doctors"])
def update_doctor(doctor_id: str, data: DoctorUpdate):
    """Update doctor details."""
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    update_data["updated_at"] = datetime.utcnow().isoformat()
    result = doctors_col.update_one(
        {"_id": str_to_objectid(doctor_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    updated = doctors_col.find_one({"_id": str_to_objectid(doctor_id)})
    return {"message": "Doctor updated successfully", "doctor": serialize(updated)}


# --- DELETE ---
@app.delete("/doctors/{doctor_id}", tags=["Doctors"])
def delete_doctor(doctor_id: str):
    """Delete a doctor."""
    result = doctors_col.delete_one({"_id": str_to_objectid(doctor_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully", "id": doctor_id}


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
