from app.services.spotify.auth import login, callback
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def auth():
    return login()

@router.get("/callback")
def cb(code: str):
    return callback(code)