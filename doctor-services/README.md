# Doctor Service
### Smart Healthcare Doctor Service
**IT4020 – Modern Topics in IT | Assignment 2**

---

## What this service does
Manages doctors and availability.
Runs on **port 8002** | Swagger UI at **http://localhost:8002/docs**

---

## Step-by-step setup (follow in order)

### Step 1 — Open VS Code terminal
Press `` Ctrl + ` `` to open the terminal inside VS Code.

### Step 2 — Go into the doctor-services folder
```
cd doctor-services
```

### Step 3 — Install dependencies
```
pip install -r requirements.txt
```

### Step 4 — Run the service
```
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
```

### Step 5 — Open Swagger UI
Go to your browser and open:
```
http://localhost:8002/docs
```

---

## API Endpoints

| Method | Endpoint               | Description                    |
|--------|------------------------|--------------------------------|
| POST   | /doctors               | Add a new doctor               |
| GET    | /doctors               | List all doctors               |
| GET    | /doctors/{id}          | Get one doctor by ID           |
| PUT    | /doctors/{id}          | Update doctor details          |
| DELETE | /doctors/{id}          | Delete a doctor                |

---

## Sample request body for POST /doctors
```json
{
  "full_name": "Dr. Nimal Perera",
  "specialization": "Cardiology",
  "email": "nimal.perera@example.com",
  "phone": "0771234567",
  "license_number": "SLMC-12345",
  "availability_status": "AVAILABLE",
  "available_from": "09:00",
  "available_to": "16:00"
}
```

---

## Database
- **MongoDB Atlas** (cloud)
- Database: `healthcare_doctor_db`
- Collection: `doctors`
- Connection is already configured in main.py

---

## Folder structure
```
doctor-services/
├── main.py           ← all the code
├── requirements.txt  ← libraries to install
└── README.md         ← this file
```
