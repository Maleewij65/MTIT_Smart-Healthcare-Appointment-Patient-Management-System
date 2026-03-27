from database import patient_collection

patient_collection.insert_one({
    "name": "Atlas Test",
    "age": 22
})

print("MongoDB Atlas Connected")