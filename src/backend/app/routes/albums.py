"""
all endpoints for showing albums and searching/filtering
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_albums():
    # all albums
    return

@router.get("/{id}")
def get_album(id: str):
    # single album with full details
    return

@router.get("/search")
def search_albums(q: str):
    # returns all albums with search (checks album name and artist name)
    return

