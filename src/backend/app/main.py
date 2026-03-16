from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv
from app.routes import spotify

app = FastAPI(title="Albumify Backend")

app.include_router(spotify.router, prefix="/spotify", tags=["SPOTIFY"])

@app.get("/")
def root():
    return {"message": "Albumify Backend Active"}
