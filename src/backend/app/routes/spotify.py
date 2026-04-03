"""
fastapi router for spotify authentication
"""

from app.services.spotify.auth import login, callback, getStatus
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def auth():
    return login()

@router.get("/callback") # used for oauth not for direct use
def cb(code: str):
    return callback(code)

@router.get("/auth/status") # returns if spotify is authenticated
def status():
    return getStatus()
