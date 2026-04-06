"""
handles getting clusters
and cluster naming
"""

from fastapi import APIRouter
from app.services.clusters_controller import get_clusters, cluster_albums, rename_cluster

router = APIRouter()

@router.get("/")
def clusters():
    # returns all clusters with name and album count
    return get_clusters()

@router.get("/{id}")
def get_cluster(id: int):
    # returns all albums in cluster
    return cluster_albums(id)

@router.post("/{id}/{name}")
def rename(id: int, name: str):
    # renames cluster
    return rename_cluster(id, name)