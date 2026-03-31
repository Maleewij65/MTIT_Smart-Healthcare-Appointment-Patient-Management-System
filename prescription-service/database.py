from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

print("MONGO_URL:", MONGODB_URL)
print("DB NAME:", DATABASE_NAME)

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

prescription_collection = db["prescriptions"]