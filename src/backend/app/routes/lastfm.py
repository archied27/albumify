"""
fast api router for lastfm services
"""

from app.services.lastfm.lastfm_api import updateDb
from fastapi import APIRouter

router = APIRouter()

@router.get("/updatedb")
def update():
    return updateDb()