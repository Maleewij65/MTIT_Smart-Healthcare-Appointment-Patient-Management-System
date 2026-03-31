import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception(" MONGO_URI not found in .env file")

# MongoDB Atlas Connection
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

# Check connection
try:
    client.admin.command("ping")
    print(" MongoDB Connected Successfully")
except Exception as e:
    print(" MongoDB Connection Failed:", e)

# Database & Collection
db = client["patient_db"]
patient_collection = db["patients"]