from app.services.spotify.auth import login, callback
from app.services.spotify.spotify_service import getSavedAlbums
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def auth():
    return login()

@router.get("/callback")
def cb(code: str):
    return callback(code)

@router.get("/get_albums")
def albums():
    return getSavedAlbums()
