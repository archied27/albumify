"""
handles getting clusters
and cluster naming
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def clusters():
    # returns all clusters with name and album count
    return

@router.get("/{id}")
def get_cluster(id: int):
    # returns all albums in cluster
    return

@router.post("/{id}/{name}")
def rename(id: int, name: str):
    # renames cluster
    return