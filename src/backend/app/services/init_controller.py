"""
initialise the database with both spotify and lastfm features
"""

from app.services.lastfm.lastfm_api import updateDb as lfmUpdateDb
from app.services.spotify.spotify_api import updateDb as sUpdateDb
from app.db.db_init import deleteAllTables, createAllTables
from app.ml.pipeline import add_clusters

status = {
    "running": False,
    "stage": None,
    "progress": None,
    "done": False,
    "error": None
}

def reset_status():
    # resets status
    global status
    status["running"] = False
    status["stage"] = None
    status["progress"] = None
    status["done"] = False
    status["error"] = None

def run_init(reset:bool):
    global status
    try:
        status["running"] = True
        status["done"] = False
        status["error"] = None

        if reset:
            status["stage"] = "Resetting Database"
            deleteAllTables()
        
        status["stage"] = "Creating Database"
        createAllTables()

        status["stage"] = "Fetching Spotify Albums"
        sUpdateDb()

        status["stage"] = "Fetching Last.fm Tags"
        lfmUpdateDb()

        status["stage"] = "Running ML Algorithm"
        add_clusters("app/db/albumify.db")

        status["stage"] = "Done"
        status["done"] = True

    except Exception as e:
        status["error"] = str(e)
        status["stage"] = "Failed"
    finally:
        status["running"] = False

def init_status():
    return status