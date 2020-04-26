from fastapi import FastAPI, Depends, Request
from routers import patients, login
from routers.login import check_if_logged_in
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.include_router(patients.router)
app.include_router(login.router)

templates = Jinja2Templates(directory="templates")


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


@app.get("/welcome", dependencies=[Depends(check_if_logged_in)])
def welcome_get(request: Request):
    username = login.router.sessions[request.cookies.get('session_token')]
    return templates.TemplateResponse("welcome.html", {"request": request, "user": username})


