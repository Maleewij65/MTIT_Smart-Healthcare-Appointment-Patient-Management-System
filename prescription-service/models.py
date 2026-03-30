from pydantic import BaseModel

class Prescription(BaseModel):
    patientId: int
    doctorId: int
    appointmentId: int
    medicine: str
    dosage: str
    instructions: str