from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
patient_list = []


class PatientPostRequest(BaseModel):
    name: str
    surename: str


class PatientPostResponse(BaseModel):
    id: int
    patient: Dict


@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/hello/{name}")
async def read_item(name: str):
    return f"Hello {name}"


@app.get("/method")
def method_get():
    return {"method": "GET"}


@app.put("/method")
def method_put():
    return {"method": "PUT"}


@app.post("/method")
def method_post():
    return {"method": "POST"}


@app.delete("/method")
def method_delete():
    return {"method": "DELETE"}


@app.get("/welcome")
def welcome_get():
    return "Jakiś powitalny tekst"


@app.post("/patient", response_model=PatientPostResponse)
def patient_post(request: PatientPostRequest):
    global patient_list
    number = len(patient_list)
    patient_list.append(request.dict())
    return PatientPostResponse(id=number, patient=patient_list[number])


@app.get("/patient/{pk}")
def patient_post(pk: int):
    global patient_list
    if 0 <= pk < len(patient_list):
        return patient_list[pk]
    raise HTTPException(status_code=204, detail="Nonexistent patient")
