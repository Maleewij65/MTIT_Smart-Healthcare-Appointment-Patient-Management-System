from fastapi import FastAPI, HTTPException
from bson import ObjectId
from models import Patient
from database import patient_collection

app = FastAPI(title="Patient Service")


# Convert MongoDB object to JSON
def patient_serializer(patient):
    return {
        "id": str(patient["_id"]),
        "name": patient["name"],
        "age": patient["age"],
        "gender": patient["gender"],
        "contact": patient["contact"],
        "email": patient["email"],
        "medicalHistory": patient.get("medicalHistory")
    }


# CREATE PATIENT
@app.post("/patients")
def create_patient(patient: Patient):
    result = patient_collection.insert_one(patient.dict())
    new_patient = patient_collection.find_one({"_id": result.inserted_id})
    return patient_serializer(new_patient)


# GET ALL PATIENTS
@app.get("/patients")
def get_patients():
    patients = patient_collection.find()
    return [patient_serializer(p) for p in patients]


# GET PATIENT BY ID
@app.get("/patients/{id}")
def get_patient(id: str):
    patient = patient_collection.find_one({"_id": ObjectId(id)})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_serializer(patient)


# UPDATE PATIENT
@app.put("/patients/{id}")
def update_patient(id: str, patient: Patient):
    patient_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": patient.dict()}
    )

    updated = patient_collection.find_one({"_id": ObjectId(id)})
    return patient_serializer(updated)


# DELETE PATIENT
@app.delete("/patients/{id}")
def delete_patient(id: str):
    patient_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Patient deleted successfully"}

@app.get("/")
def home():
    return {
        "status": "Patient Service is running",
        "docs": "/docs"
    }