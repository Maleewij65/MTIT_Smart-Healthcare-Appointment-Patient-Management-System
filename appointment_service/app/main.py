from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn

# ✅ FIXED IMPORTS (IMPORTANT)
from .database import appointments_col, str_to_objectid, serialize, serialize_list
from .models import AppointmentCreate, AppointmentUpdate

# ── App setup ──────────────────────────────────────────
app = FastAPI(
    title="Appointment Service",
    description="Smart Healthcare – Appointment & Patient Management System",
    version="1.0.0",
)

# ── Routes ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Appointment Service",
        "status": "running",
        "port": 8004
    }


# --- CREATE ---
@app.post("/appointments", tags=["Appointments"], status_code=201)
def create_appointment(data: AppointmentCreate):
    """Book a new appointment."""
    doc = data.dict()
    doc["created_at"] = datetime.utcnow().isoformat()

    result = appointments_col.insert_one(doc)
    created = appointments_col.find_one({"_id": result.inserted_id})

    return {
        "message": "Appointment created successfully",
        "appointment": serialize(created)
    }


# --- GET ALL ---
@app.get("/appointments", tags=["Appointments"])
def get_all_appointments():
    """List all appointments."""
    docs = list(appointments_col.find())
    return {
        "total": len(docs),
        "appointments": serialize_list(docs)
    }


# --- GET ONE ---
@app.get("/appointments/{appointment_id}", tags=["Appointments"])
def get_appointment(appointment_id: str):
    """Get a single appointment by ID."""
    doc = appointments_col.find_one({"_id": str_to_objectid(appointment_id)})

    if not doc:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return serialize(doc)


# --- GET BY PATIENT ---
@app.get("/appointments/patient/{patient_id}", tags=["Appointments"])
def get_appointments_by_patient(patient_id: str):
    """Get all appointments for a specific patient."""
    docs = list(appointments_col.find({"patient_id": patient_id}))

    if not docs:
        raise HTTPException(
            status_code=404,
            detail="No appointments found for this patient"
        )

    return {
        "patient_id": patient_id,
        "total": len(docs),
        "appointments": serialize_list(docs)
    }


# --- GET BY DOCTOR ---
@app.get("/appointments/doctor/{doctor_id}", tags=["Appointments"])
def get_appointments_by_doctor(doctor_id: str):
    """Get all appointments for a specific doctor."""
    docs = list(appointments_col.find({"doctor_id": doctor_id}))

    if not docs:
        raise HTTPException(
            status_code=404,
            detail="No appointments found for this doctor"
        )

    return {
        "doctor_id": doctor_id,
        "total": len(docs),
        "appointments": serialize_list(docs)
    }


# --- UPDATE ---
@app.put("/appointments/{appointment_id}", tags=["Appointments"])
def update_appointment(appointment_id: str, data: AppointmentUpdate):
    """Reschedule or update an appointment."""
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided to update"
        )

    update_data["updated_at"] = datetime.utcnow().isoformat()

    result = appointments_col.update_one(
        {"_id": str_to_objectid(appointment_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")

    updated = appointments_col.find_one(
        {"_id": str_to_objectid(appointment_id)}
    )

    return {
        "message": "Appointment updated successfully",
        "appointment": serialize(updated)
    }


# --- DELETE ---
@app.delete("/appointments/{appointment_id}", tags=["Appointments"])
def delete_appointment(appointment_id: str):
    """Cancel and delete an appointment."""
    result = appointments_col.delete_one(
        {"_id": str_to_objectid(appointment_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return {
        "message": "Appointment deleted successfully",
        "id": appointment_id
    }


# ── Run ────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",   # ✅ IMPORTANT FIX
        host="0.0.0.0",
        port=8004,
        reload=True
    )