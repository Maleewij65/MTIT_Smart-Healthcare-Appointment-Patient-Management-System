from pymongo import MongoClient
from bson import ObjectId

# -------------------------------
# DATABASE
# -------------------------------

client = MongoClient("mongodb+srv://Hospital_MTIT:hospital123@cluster0.lnhqemi.mongodb.net/?retryWrites=true&w=majority")
db = client["healthcare_billing_Service_db"]

collection = db["billing"]


# -------------------------------
# SERIALIZER (IMPORTANT FIX)
# -------------------------------
def serialize(bill) -> dict:
    return {
        "id": str(bill["_id"]),
        "patient_id": bill["patient_id"],
        "appointment_id": bill["appointment_id"],
        "doctor_id": bill["doctor_id"],
        "description": bill["description"],
        "amount": bill["amount"],
        "payment_method": bill["payment_method"],
        "payment_status": bill["payment_status"],
    }


# -------------------------------
# CREATE BILL
# -------------------------------
def create_bill(data):
    bill = data.dict()
    result = collection.insert_one(bill)
    new_bill = collection.find_one({"_id": result.inserted_id})
    return serialize(new_bill)


# -------------------------------
# GET ALL
# -------------------------------
def get_all_bills():
    return [serialize(b) for b in collection.find()]


# -------------------------------
# GET ONE
# -------------------------------
def get_bill(bill_id: str):
    bill = collection.find_one({"_id": ObjectId(bill_id)})
    if bill:
        return serialize(bill)
    return {"message": "Bill not found"}


# -------------------------------
# UPDATE
# -------------------------------
def update_bill(bill_id: str, data):
    collection.update_one(
        {"_id": ObjectId(bill_id)},
        {"$set": data.dict(exclude_none=True)}
    )
    updated = collection.find_one({"_id": ObjectId(bill_id)})
    return serialize(updated)


# -------------------------------
# DELETE
# -------------------------------
def delete_bill(bill_id: str):
    collection.delete_one({"_id": ObjectId(bill_id)})
    return {"message": "Bill deleted successfully"}


# -------------------------------
# MARK AS PAID
# -------------------------------
def mark_paid(bill_id: str, payment_method: str):
    collection.update_one(
        {"_id": ObjectId(bill_id)},
        {"$set": {"payment_status": "paid", "payment_method": payment_method}}
    )
    updated = collection.find_one({"_id": ObjectId(bill_id)})
    return serialize(updated)