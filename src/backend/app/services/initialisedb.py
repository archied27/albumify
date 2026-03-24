"""
initialise the database with both spotify and lastfm features
"""

from app.services.lastfm.lastfm_api import updateDb as lfmUpdateDb
from app.services.spotify.spotify_api import updateDb as sUpdateDb

def initDb():
    sUpdateDb()
    lfmUpdateDb()
