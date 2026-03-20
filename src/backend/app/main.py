from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv
from app.routes import spotify, lastfm

app = FastAPI(title="Albumify Backend")

app.include_router(spotify.router, prefix="/spotify", tags=["SPOTIFY"])
app.include_router(lastfm.router, prefix="/lastfm", tags=["LASTFM"])

@app.get("/")
def root():
    return {"message": "Albumify Backend Active"}
