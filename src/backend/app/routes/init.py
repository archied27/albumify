"""
router for initialising database with all album info and clustering
"""

from fastapi import APIRouter, BackgroundTasks
from app.services.init_controller import init_status, run_init, reset_status
from app.ml.pipeline import add_clusters

router = APIRouter()

@router.post("/")
def init(background_tasks: BackgroundTasks):
    # start full init
    # background task
    if init_status()["running"]:
        return{
            "message": "already running",
            "stage": status["stage"]
        }

    reset_status()
    background_tasks.add_task(run_init, reset=False)
    return {"message": "initialisation started"}

@router.get("/status")
def status():
    # returns current status of init
    return init_status()

@router.post("/reset")
def reset(background_tasks: BackgroundTasks):
    # resets all tables and reruns init
    if init_status()["running"]:
        return {"message": "already running"}

    reset_status()
    background_tasks.add_task(run_init, reset=True)
    return {"message": "reset started"}

@router.post("/recluster")
def recluster():
    print("reclustering")
    add_clusters("app/db/albumify.db")