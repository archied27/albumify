"""
all endpoints for showing albums and searching/filtering
"""

from fastapi import APIRouter
from app.services.albums_controller import get_all_albums, get_album_info, search_albums

router = APIRouter()

@router.get("/")
def get_albums():
    # all albums
    return get_all_albums()

@router.get("/search")
def search(q: str):
    # returns all albums with search (checks album name and artist name)
    return search_albums(q)

@router.get("/{id}")
def get_album(id: str):
    # single album with full details
    return get_album_info(id)