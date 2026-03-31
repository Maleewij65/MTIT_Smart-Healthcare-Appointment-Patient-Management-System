# MTIT_Smart-Healthcare-Appointment-Patient-Management-System


## Overview

The Smart Healthcare Appointment and Patient Management System is a microservices-based healthcare platform developed using FastAPI. The system integrates multiple healthcare functionalities including patient management, doctor management, appointment scheduling, prescription handling, and billing services through a centralized API Gateway.

This project demonstrates modern distributed system architecture where independent services communicate using REST APIs while remaining loosely coupled and independently deployable.

---

## System Architecture

The system follows a microservices architecture with a single API Gateway acting as the entry point for all client requests.

Client applications such as web apps, mobile apps, or Postman send requests to the API Gateway, which routes them to the appropriate microservice.

Architecture Flow:

Client Layer  
        |  
        v  
API Gateway (Port 8000)  
        |  
-------------------------------------------------------------  
|        |         |         |         |  
Patient  Doctor  Prescription Appointment Billing  
Service  Service     Service     Service     Service  
8001     8002        8003        8004        8005  

Each service maintains its own database to ensure data isolation.

---

## Microservices Components

### Patient Service (Port 8001)
Handles patient-related operations:
- Create patient profile
- View patient details
- Update patient information
- Delete patient records

Endpoints:
POST /patients  
GET /patients/{id}  
PUT /patients/{id}  
DELETE /patients/{id}

---

### Doctor Service (Port 8002)
Manages doctor information and availability:
- Add doctor
- View doctors
- Update specialization or availability
- Remove doctor

Endpoints:
POST /doctors  
GET /doctors/{id}  
PUT /doctors/{id}  
DELETE /doctors/{id}

---

### Prescription Service (Port 8003)
Stores and manages prescriptions:
- Add prescription
- View prescriptions
- Update medication details
- Delete prescription

Endpoints:
POST /prescriptions  
GET /prescriptions/{id}  
PUT /prescriptions/{id}  
DELETE /prescriptions/{id}

---

### Appointment Service (Port 8004)
Handles appointment booking logic:
- Create appointments
- View appointments
- Reschedule appointments
- Cancel appointments

Endpoints:
POST /appointments  
GET /appointments/{id}  
PUT /appointments/{id}  
DELETE /appointments/{id}

---

### Billing Service (Port 8005)
Manages billing and payment operations:
- Create bills
- View payment status
- Update payments
- Delete bills

Endpoints:
POST /billing  
GET /billing/{id}  
PUT /billing/{id}  
DELETE /billing/{id}

---

## API Gateway

The API Gateway provides a unified access point to all microservices.

Responsibilities:
- Single entry point for clients
- Request routing to services
- Hiding internal service ports
- Centralized API documentation
- Improved scalability

Example Routes:

/api/patients       -> Patient Service  
/api/doctors        -> Doctor Service  
/api/prescriptions  -> Prescription Service  
/api/appointments   -> Appointment Service  
/api/billing        -> Billing Service

---

## Technologies Used

- Python 3.x
- FastAPI
- Uvicorn
- MongoDB
- HTTPX (Async HTTP Client)
- Pydantic
- OpenAPI / Swagger UI

---

## Project Structure

MTIT_Smart-Healthcare-Appointment-Patient-Management-System/

api-gateway/  
patient-service/  
doctor-services/  
prescription-service/  
appointment-service/  
billing-service/  
README.md  

---

## Setup Instructions

### Clone Repository

git clone <repository-url>  
cd MTIT_Smart-Healthcare-Appointment-Patient-Management-System

---

### Create Virtual Environment (for each service)

python -m venv venv

Activate on Windows:

venv\Scripts\activate

---

### Install Dependencies

pip install -r requirements.txt

---

## Running the System

Start each service in a separate terminal.

### Patient Service
cd patient-service  
uvicorn app.main:app --reload --port 8001

### Doctor Service
cd doctor-services  
uvicorn app.main:app --reload --port 8002

### Prescription Service
cd prescription-service  
uvicorn app.main:app --reload --port 8003

### Appointment Service
cd appointment-service  
uvicorn app.main:app --reload --port 8004

### Billing Service
cd billing-service  
uvicorn app.main:app --reload --port 8005

### API Gateway (start last)
cd api-gateway  
uvicorn main:app --reload --port 8000

---

## Accessing the Application

API Gateway Root:
http://127.0.0.1:8000

Swagger Documentation:
http://127.0.0.1:8000/docs

All APIs can be accessed through the gateway documentation.

---

## Example Request

Create Patient

POST /api/patients

Request Body:

{
  "name": "John Doe",
  "age": 30,
  "gender": "Male",
  "contact": "0771234567",
  "email": "john@example.com"
}

---

## Key Features

- Microservices-based architecture
- Independent service deployment
- Centralized API Gateway
- RESTful API design
- Data isolation per service
- Automatic API documentation

---

## Future Improvements

- JWT Authentication
- Docker containerization
- Service discovery
- Load balancing
- Centralized logging
- Cloud deployment

---

## Academic Purpose

This project was developed as part of an academic assignment to demonstrate microservices architecture concepts and healthcare system integration using modern backend technologies.

---

## Contributors

Doctor Service – IT22926012
Patient Service – IT22339324 
Appointment Service – IT22187550  
Prescription Service – IT22222190  
Billing Service – IT22236128
