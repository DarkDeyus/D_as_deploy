from typing import Dict
from fastapi import HTTPException, APIRouter, Depends, Response, status
from pydantic import BaseModel
from routers.login import check_if_logged_in

router = APIRouter()
router.patients: Dict[str, dict] = {}
router.next_id_number = 0


class PatientPostRequest(BaseModel):
    name: str
    surname: str


class PatientPostResponse(BaseModel):
    name: str
    surname: str


@router.post("/patient", response_model=PatientPostResponse, dependencies=[Depends(check_if_logged_in)])
def patient_post(request: PatientPostRequest, response: Response):

    number = router.next_id_number
    router.next_id_number += 1
    router.patients[f"id_{number}"] = request.dict()

    response.headers['Location'] = f"/patient/{number}"
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY

    return PatientPostResponse(name=request.name, surname=request.surname)


@router.get("/patient", dependencies=[Depends(check_if_logged_in)])
def patient_get_id():
    return router.patients


@router.get("/patient/{patient_id}", dependencies=[Depends(check_if_logged_in)])
def patient_get_id(patient_id: int):
    key = f"id_{patient_id}"
    if key in router.patients:
        return router.patients[key]


@router.delete("/patient/{patient_id}", dependencies=[Depends(check_if_logged_in)])
def patient_delete_id(response: Response, patient_id: int):
    key = f"id_{patient_id}"
    router.patients.pop(key)
    response.status_code = status.HTTP_204_NO_CONTENT

