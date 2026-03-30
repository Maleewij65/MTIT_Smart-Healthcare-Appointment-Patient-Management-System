from fastapi import FastAPI
import uvicorn
import webbrowser
import threading

import models
import database

# -------------------------------
# APP SETUP
# -------------------------------
app = FastAPI(
    title="Billing Service",
    description="Smart Healthcare – Billing & Payment Management System",
    version="1.0.0",
)

# -------------------------------
# AUTO OPEN SWAGGER
# -------------------------------
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8005/docs")


@app.on_event("startup")
def startup():
    threading.Timer(1.5, open_browser).start()


# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def root():
    return {"service": "Billing Service", "status": "running"}


# -------------------------------
# ROUTES
# -------------------------------
@app.post("/billing", response_model=models.BillResponse)
def create_bill(data: models.BillCreate):
    return database.create_bill(data)


@app.get("/billing", response_model=list[models.BillResponse])
def get_all():
    return database.get_all_bills()


@app.get("/billing/{bill_id}", response_model=models.BillResponse)
def get_one(bill_id: str):
    return database.get_bill(bill_id)


@app.put("/billing/{bill_id}", response_model=models.BillResponse)
def update(bill_id: str, data: models.BillUpdate):
    return database.update_bill(bill_id, data)


@app.delete("/billing/{bill_id}")
def delete(bill_id: str):
    return database.delete_bill(bill_id)


@app.put("/billing/{bill_id}/pay", response_model=models.BillResponse)
def pay(bill_id: str, payment_method: str = "cash"):
    return database.mark_paid(bill_id, payment_method)


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)