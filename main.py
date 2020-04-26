from typing import Dict
from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, status
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from routers import patients, login
import secrets

app = FastAPI()
app.include_router(patients.router)
app.include_router(login.router)


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


