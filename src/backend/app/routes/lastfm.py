"""
fast api router for lastfm services
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/updatedb")
def update():
    return