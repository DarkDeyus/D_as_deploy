from typing import Set
from fastapi import HTTPException, Response, Cookie, Depends, status, APIRouter, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
from starlette.responses import RedirectResponse
import secrets


router = APIRouter()
security = HTTPBasic()

router.secret_key = "You will never guess it! It is just impossible to do so!"

session_tokens: Set[str] = set()


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
    return session_token


def check_session_token(token: str):
    if token not in session_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    return token


@router.post("/login")
def login(response: Response, session_token: str = Depends(check_login_data)):
    response.set_cookie(key='session_token', value=session_token)
    response.headers['Location'] = "/welcome"
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY
    session_tokens.add(session_token)


@router.post("/logout")
def logout(response: Response, request: Request):
    token = check_session_token(request.cookies.get('session_token'))
    session_tokens.remove(token)

    response.headers['Location'] = '/'
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY
