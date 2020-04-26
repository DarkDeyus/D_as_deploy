from typing import Dict
from fastapi import HTTPException, APIRouter, Depends, Response, status
from pydantic import BaseModel
from routers.login import check_if_logged_in

router = APIRouter()

patients: Dict[str, dict] = {}

next_id_number = 0


class PatientPostRequest(BaseModel):
    name: str
    surname: str


class PatientPostResponse(BaseModel):
    name: str
    surname: str


@router.post("/patient", response_model=PatientPostResponse, dependencies=[Depends(check_if_logged_in)])
def patient_post(request: PatientPostRequest, response: Response):
    global patients, next_id
    number = next_id
    next_id += 1
    patients[f"id_{number}"] = request.dict()

    response.headers['Location'] = f"/patient/{number}"
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY

    return PatientPostResponse(name=request.name, surname=request.surname)


@router.get("/patient", dependencies=[Depends(check_if_logged_in)])
def patient_get_id():
    global patients
    return patients



@router.get("/patient/{pk}", dependencies=[Depends(check_if_logged_in)])
def patient_get_id(pk: int):
    global patients
    key = f"id_{pk}"
    if key in patients:
        return patients[key]
    else:
        raise HTTPException(status_code=204, detail="Nonexistent patient")


@router.delete("/patient/{pk}", dependencies=[Depends(check_if_logged_in)])
def patient_delete_id(pk: int):
    global patients
    key = f"id_{pk}"
    if key in patients:
        patients.pop(key)
    else:
        raise HTTPException(status_code=204, detail="Nonexistent patient")
