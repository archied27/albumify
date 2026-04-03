from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv
from app.routes import spotify, albums, clusters, init

app = FastAPI(title="Albumify Backend")

app.include_router(spotify.router, prefix="/spotify", tags=["SPOTIFY"])
app.include_router(albums.router, prefix="/albums", tags=["ALBUMS"])
app.include_router(clusters.router, prefix="/clusters", tags=["CLUSTERS"])
app.include_router(init.router, prefix="/init", tags=["INIT"])

@app.get("/")
def root():
    return {"message": "Albumify Backend Active"}
