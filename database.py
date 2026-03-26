from pymongo import MongoClient

# Connect to MongoDB (local)
client = MongoClient("mongodb://localhost:27017")

# Database
db = client["patient_db"]

# Collection
patient_collection = db["patients"]