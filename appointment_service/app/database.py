from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
import os

# ── MongoDB Atlas Connection ───────────────────────────

# 🔒 Better practice: use environment variable (fallback included)
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://Hospital_MTIT:hospital123@cluster0.lnhqemi.mongodb.net/?retryWrites=true&w=majority"
)

try:
    client = MongoClient(MONGO_URI)
    db = client["healthcare_db"]
    appointments_col = db["appointments"]
except Exception as e:
    raise Exception(f"Database connection failed: {e}")

# ── Helpers ────────────────────────────────────────────

def str_to_objectid(id: str) -> ObjectId:
    """Convert string ID to MongoDB ObjectId with validation."""
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid ID format: {id}"
        )

def serialize(doc: dict) -> dict:
    """Convert MongoDB document _id to string id."""
    if not doc:
        return doc

    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

def serialize_list(docs):
    """Convert list of MongoDB documents."""
    return [serialize(doc) for doc in docs]