# Appointment Service
### Smart Healthcare Appointment & Patient Management System
**IT4020 – Modern Topics in IT | Assignment 2**

---

## What this service does
Manages appointments between patients and doctors.
Runs on **port 8003** | Swagger UI at **http://localhost:8003/docs**

---

## Step-by-step setup (follow in order)

### Step 1 — Open VS Code terminal
Press `` Ctrl + ` `` to open the terminal inside VS Code.

### Step 2 — Go into the appointment-service folder
```
cd appointment-service
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
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
```

### Step 5 — Open Swagger UI
Go to your browser and open:
```
http://localhost:8003/docs
```
This is where you take screenshots for the slides!

---

## API Endpoints

| Method | Endpoint                            | Description                        |
|--------|-------------------------------------|------------------------------------|
| POST   | /appointments                       | Book a new appointment             |
| GET    | /appointments                       | List all appointments              |
| GET    | /appointments/{id}                  | Get one appointment by ID          |
| GET    | /appointments/patient/{patient_id}  | All appointments for a patient     |
| GET    | /appointments/doctor/{doctor_id}    | All appointments for a doctor      |
| PUT    | /appointments/{id}                  | Reschedule / update appointment    |
| DELETE | /appointments/{id}                  | Cancel / delete appointment        |

---

## Sample request body for POST /appointments
```json
{
  "patient_id": "p001",
  "doctor_id": "d001",
  "appointment_date": "2026-04-10",
  "appointment_time": "10:30",
  "reason": "Routine check-up",
  "status": "scheduled"
}
```

---

## Database
- **MongoDB Atlas** (cloud)
- Database: `healthcare_db`
- Collection: `appointments`
- Connection is already configured in main.py

---

## Folder structure
```
appointment-service/
├── main.py           ← all the code
├── requirements.txt  ← libraries to install
└── README.md         ← this file
```
