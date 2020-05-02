from fastapi import FastAPI, Depends, Request
from routers import patients, login, tracks, albums
from routers.login import check_if_logged_in
from fastapi.templating import Jinja2Templates
import database as db
import aiosqlite

app = FastAPI()
app.include_router(patients.router)
app.include_router(login.router)
app.include_router(tracks.router)
app.include_router(albums.router)

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    db.DB_CONNECTION = await aiosqlite.connect(db.DB_ADDRESS)


@app.on_event("shutdown")
async def shutdown():
    await db.DB_CONNECTION.close()


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
    sessions = login.router.get_sessions()
    username = sessions[request.cookies.get('session_token')]
    return templates.TemplateResponse("welcome.html", {"request": request, "user": username})


