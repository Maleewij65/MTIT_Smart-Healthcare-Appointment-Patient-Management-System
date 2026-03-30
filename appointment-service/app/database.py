from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

# ── MongoDB Atlas Connection ───────────────────────────
MONGO_URI = "mongodb+srv://Hospital_MTIT:hospital123@cluster0.lnhqemi.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["healthcare_db"]
appointments_col = db["appointments"]

# ── Helpers ────────────────────────────────────────────
def str_to_objectid(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {id}")

def serialize(doc) -> dict:
    """Convert MongoDB document _id to string id."""
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc
