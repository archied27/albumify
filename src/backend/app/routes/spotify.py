"""
fastapi router for spotify services
"""

from app.services.spotify.auth import login, callback
from app.services.spotify.spotify_api import updateDb
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def auth():
    return login()

@router.get("/callback") # used for oauth not for direct use
def cb(code: str):
    return callback(code)

@router.get("/updatedb") # stores all spotify features into db
def albums():
    return updateDb()
