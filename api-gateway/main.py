from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse
from typing import Dict, Any
import httpx

app = FastAPI(
    title="API Gateway",
    description="Unified Access to Smart Healthcare Microservices",
    version="1.0.0"
)

# -------------------------------
# SERVICE URLs
# -------------------------------
PATIENT_SERVICE = "http://127.0.0.1:8001"
DOCTOR_SERVICE = "http://127.0.0.1:8002"
PRESCRIPTION_SERVICE = "http://127.0.0.1:8003"
APPOINTMENT_SERVICE = "http://127.0.0.1:8004"
BILLING_SERVICE = "http://127.0.0.1:8005"


# -------------------------------
# COMMON PROXY FUNCTION
# -------------------------------
async def proxy_request(base_url: str, path: str, request: Request):

    async with httpx.AsyncClient() as client:

        url = f"{base_url}/{path}" if path else base_url

        try:
            print(f"{request.method} → {url}")

            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.json()
                response = await client.request(
                    method=request.method,
                    url=url,
                    json=body
                )
            else:
                response = await client.request(
                    method=request.method,
                    url=url
                )

            try:
                content = response.json()
            except:
                content = response.text

            return JSONResponse(
                status_code=response.status_code,
                content=content
            )

        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"gateway_error": str(e)}
            )


# =====================================================
# PATIENT SERVICE
# =====================================================
@app.post("/api/patients")
async def create_patient(request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(PATIENT_SERVICE, "patients", request)


@app.get("/api/patients")
async def get_patients(request: Request):
    return await proxy_request(PATIENT_SERVICE, "patients", request)


@app.get("/api/patients/{id}")
async def get_patient(id: str, request: Request):
    return await proxy_request(PATIENT_SERVICE, f"patients/{id}", request)


@app.put("/api/patients/{id}")
async def update_patient(id: str, request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(PATIENT_SERVICE, f"patients/{id}", request)


@app.delete("/api/patients/{id}")
async def delete_patient(id: str, request: Request):
    return await proxy_request(PATIENT_SERVICE, f"patients/{id}", request)



# =====================================================
# DOCTOR SERVICE
# =====================================================
@app.post("/api/doctors")
async def create_doctor(request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(DOCTOR_SERVICE, "doctors", request)


@app.get("/api/doctors")
async def get_doctors(request: Request):
    return await proxy_request(DOCTOR_SERVICE, "doctors", request)


@app.get("/api/doctors/{id}")
async def get_doctor(id: str, request: Request):
    return await proxy_request(DOCTOR_SERVICE, f"doctors/{id}", request)


@app.put("/api/doctors/{id}")
async def update_doctor(id: str, request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(DOCTOR_SERVICE, f"doctors/{id}", request)


@app.delete("/api/doctors/{id}")
async def delete_doctor(id: str, request: Request):
    return await proxy_request(DOCTOR_SERVICE, f"doctors/{id}", request)


# =====================================================
# PRESCRIPTION SERVICE
# =====================================================

@app.post("/api/prescriptions")
async def create_prescription(request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(PRESCRIPTION_SERVICE, "api/prescriptions", request)


@app.get("/api/prescriptions")
async def get_prescriptions(request: Request):
    return await proxy_request(PRESCRIPTION_SERVICE, "api/prescriptions", request)


@app.get("/api/prescriptions/{id}")
async def get_prescription(id: str, request: Request):
    return await proxy_request(PRESCRIPTION_SERVICE, f"api/prescriptions/{id}", request)


@app.put("/api/prescriptions/{id}")
async def update_prescription(id: str, request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(PRESCRIPTION_SERVICE, f"api/prescriptions/{id}", request)


@app.delete("/api/prescriptions/{id}")
async def delete_prescription(id: str, request: Request):
    return await proxy_request(PRESCRIPTION_SERVICE, f"api/prescriptions/{id}", request)



# =====================================================
# APPOINTMENT SERVICE
# =====================================================
@app.post("/api/appointments")
async def create_appointment(request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(APPOINTMENT_SERVICE, "appointments", request)


@app.get("/api/appointments")
async def get_appointments(request: Request):
    return await proxy_request(APPOINTMENT_SERVICE, "appointments", request)


@app.get("/api/appointments/{id}")
async def get_appointment(id: str, request: Request):
    return await proxy_request(APPOINTMENT_SERVICE, f"appointments/{id}", request)


@app.put("/api/appointments/{id}")
async def update_appointment(id: str, request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(APPOINTMENT_SERVICE, f"appointments/{id}", request)


@app.delete("/api/appointments/{id}")
async def delete_appointment(id: str, request: Request):
    return await proxy_request(APPOINTMENT_SERVICE, f"appointments/{id}", request)


# =====================================================
# BILLING SERVICE
# =====================================================
@app.post("/api/billing")
async def create_bill(request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(BILLING_SERVICE, "billing", request)


@app.get("/api/billing")
async def get_bills(request: Request):
    return await proxy_request(BILLING_SERVICE, "billing", request)


@app.get("/api/billing/{id}")
async def get_bill(id: str, request: Request):
    return await proxy_request(BILLING_SERVICE, f"billing/{id}", request)


@app.put("/api/billing/{id}")
async def update_bill(id: str, request: Request, body: Dict[str, Any] = Body(...)):
    return await proxy_request(BILLING_SERVICE, f"billing/{id}", request)


@app.delete("/api/billing/{id}")
async def delete_bill(id: str, request: Request):
    return await proxy_request(BILLING_SERVICE, f"billing/{id}", request)



# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def root():
    return {
        "message": "API Gateway is running successfully",
        "services": [
            "Patient Service",
            "Doctor Service",
            "Prescription Service",
            "Appointment Service",
            "Billing Service"
        ]
    }