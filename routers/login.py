from typing import Set, Dict
from fastapi import HTTPException, Response, Depends, status, APIRouter, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
import secrets

router = APIRouter()
router.secret_key = "You will never guess it! It is just impossible to do so!"
router.sessions: Dict[str, str] = {}

security = HTTPBasic()


def check_login_data(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not correct_username or not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{router.secret_key}",
                                 encoding='utf-8')).hexdigest()
    return session_token, credentials.username


def check_if_logged_in(request: Request):
    token = request.cookies.get('session_token')
    if token not in router.sessions:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    return token


@router.post("/login")
def login(response: Response, session: (str, str) = Depends(check_login_data)):
    session_token, username = session
    response.set_cookie(key='session_token', value=session_token)
    response.headers['Location'] = "/welcome"
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY

    if session_token not in router.sessions:
        router.sessions[session_token] = username


@router.post("/logout", dependencies=[Depends(check_if_logged_in)])
def logout(response: Response, request: Request):
    token = request.cookies.get('session_token')
    router.sessions.remove(token)

    response.headers['Location'] = '/'
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY
