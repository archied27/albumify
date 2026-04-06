from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv
from app.routes import spotify, albums, clusters, init

app = FastAPI(title="Albumify Backend")

origins = [
    "http://localhost:3000", 
    "http://localhost:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spotify.router, prefix="/spotify", tags=["SPOTIFY"])
app.include_router(albums.router, prefix="/albums", tags=["ALBUMS"])
app.include_router(clusters.router, prefix="/clusters", tags=["CLUSTERS"])
app.include_router(init.router, prefix="/init", tags=["INIT"])

@app.get("/")
def root():
    return {"message": "Albumify Backend Active"}
