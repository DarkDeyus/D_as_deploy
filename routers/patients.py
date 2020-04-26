from typing import Dict
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter()

patient_list = []


class PatientPostRequest(BaseModel):
    name: str
    surename: str


class PatientPostResponse(BaseModel):
    id: int
    patient: Dict


@router.post("/patient", response_model=PatientPostResponse)
def patient_post(request: PatientPostRequest):
    global patient_list
    number = len(patient_list)
    patient_list.append(request.dict())
    return PatientPostResponse(id=number, patient=patient_list[number])


@router.get("/patient/{pk}")
def patient_post(pk: int):
    global patient_list
    if 0 <= pk < len(patient_list):
        return patient_list[pk]
    raise HTTPException(status_code=204, detail="Nonexistent patient")