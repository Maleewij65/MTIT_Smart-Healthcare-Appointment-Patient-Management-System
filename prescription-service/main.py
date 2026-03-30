from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from models import Prescription
import os

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# -----------------------------
# MongoDB Connection
# -----------------------------
client = MongoClient(MONGODB_URL)

app = FastAPI(title="Prescription Service")

# -----------------------------
# Connection check on startup
# -----------------------------
@app.on_event("startup")
def connect_to_db():
    try:
        client.admin.command("ping")
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

# -----------------------------
# DB & Collection
# -----------------------------
db = client[DATABASE_NAME]
collection = db["prescriptions"]

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "Prescription Service Running"}

# -----------------------------
# Test DB Connection
# -----------------------------
@app.get("/test-db")
def test_db():
    try:
        collections = db.list_collection_names()
        return {
            "status": "connected",
            "collections": collections
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -----------------------------
# Create Prescription
# -----------------------------
@app.post("/api/prescriptions")
def create_prescription(data: Prescription):
    result = collection.insert_one(data.dict())
    return {
        "message": "Prescription created",
        "id": str(result.inserted_id)
    }

# -----------------------------
# Get All Prescriptions
# -----------------------------
@app.get("/api/prescriptions")
def get_all_prescriptions():
    prescriptions = list(collection.find())
    
    for p in prescriptions:
        p["_id"] = str(p["_id"])
    
    return prescriptions

# -----------------------------
# Get Prescription by ID
# -----------------------------
@app.get("/api/prescriptions/{id}")
def get_prescription(id: str):
    try:
        prescription = collection.find_one({"_id": ObjectId(id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if not prescription:
        raise HTTPException(status_code=404, detail="Not found")

    prescription["_id"] = str(prescription["_id"])
    return prescription

# -----------------------------
# Get by Patient ID
# -----------------------------
@app.get("/api/prescriptions/patient/{patientId}")
def get_by_patient(patientId: int):
    prescriptions = list(collection.find({"patientId": patientId}))
    
    for p in prescriptions:
        p["_id"] = str(p["_id"])
    
    return prescriptions

# -----------------------------
# Get by Appointment ID
# -----------------------------
@app.get("/api/prescriptions/appointment/{appointmentId}")
def get_by_appointment(appointmentId: int):
    prescriptions = list(collection.find({"appointmentId": appointmentId}))
    
    for p in prescriptions:
        p["_id"] = str(p["_id"])
    
    return prescriptions

# -----------------------------
# Update Prescription
# -----------------------------
@app.put("/api/prescriptions/{id}")
def update_prescription(id: str, data: dict):
    try:
        result = collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Prescription updated"}

# -----------------------------
# Delete Prescription
# -----------------------------
@app.delete("/api/prescriptions/{id}")
def delete_prescription(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Prescription deleted"}