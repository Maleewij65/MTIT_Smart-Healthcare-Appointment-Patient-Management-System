from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from typing import List

from app.models import Patient, PatientResponse
from app.database import patient_collection

app = FastAPI(
    title="Patient Service",
    description="Smart Healthcare Patient Management Microservice",
    version="1.1.0"
)


# -------------------------------
# Helper Functions
# -------------------------------

def validate_object_id(id: str) -> ObjectId:
    """Validate MongoDB ObjectId"""
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid patient ID format"
        )
    return ObjectId(id)


def patient_serializer(patient) -> dict:
    """Convert MongoDB document to JSON"""
    return {
        "id": str(patient["_id"]),
        "name": patient["name"],
        "age": patient["age"],
        "gender": patient["gender"],
        "contact": patient["contact"],
        "email": patient["email"],
        "medicalHistory": patient.get("medicalHistory")
    }


# -------------------------------
# CREATE PATIENT
# -------------------------------
@app.post(
    "/patients",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED
)
def create_patient(patient: Patient):

    result = patient_collection.insert_one(patient.dict())
    new_patient = patient_collection.find_one(
        {"_id": result.inserted_id}
    )

    return patient_serializer(new_patient)


# -------------------------------
# GET ALL PATIENTS
# -------------------------------
@app.get(
    "/patients",
    response_model=List[PatientResponse]
)
def get_patients():

    patients = patient_collection.find()
    return [patient_serializer(p) for p in patients]


# -------------------------------
# PATIENT STATISTICS (🔥 MOVED UP)
# -------------------------------
@app.get("/patients/stats")
def get_patient_stats():
    """
    Returns analytical statistics about patients
    """

    total = patient_collection.count_documents({})

    male_count = patient_collection.count_documents({
        "gender": {"$regex": "^male$", "$options": "i"}
    })

    female_count = patient_collection.count_documents({
        "gender": {"$regex": "^female$", "$options": "i"}
    })

    senior_count = patient_collection.count_documents({
        "age": {"$gt": 60}
    })

    return {
        "totalPatients": total,
        "malePatients": male_count,
        "femalePatients": female_count,
        "seniorPatients": senior_count
    }


# -------------------------------
# GET PATIENT BY ID (🔥 MOVED DOWN)
# -------------------------------
@app.get(
    "/patients/{id}",
    response_model=PatientResponse
)
def get_patient(id: str):

    object_id = validate_object_id(id)

    patient = patient_collection.find_one({"_id": object_id})

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient_serializer(patient)


# -------------------------------
# UPDATE PATIENT
# -------------------------------
@app.put(
    "/patients/{id}",
    response_model=PatientResponse
)
def update_patient(id: str, patient: Patient):

    object_id = validate_object_id(id)

    result = patient_collection.update_one(
        {"_id": object_id},
        {"$set": patient.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    updated_patient = patient_collection.find_one({"_id": object_id})

    return patient_serializer(updated_patient)


# -------------------------------
# DELETE PATIENT
# -------------------------------
@app.delete("/patients/{id}")
def delete_patient(id: str):

    object_id = validate_object_id(id)

    result = patient_collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return {"message": "Patient deleted successfully"}


# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def home():
    return {
        "status": "Patient Service is running",
        "docs": "/docs"
    }