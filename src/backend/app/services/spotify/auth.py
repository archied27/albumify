"""
Handles authenticating user with Spotify's API
"""
import os
import requests
import fastapi
import dotenv
from urllib.parse import urlencode

dotenv.load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-library-read"

def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }

    auth_url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return fastapi.responses.RedirectResponse(auth_url)

def callback(code: str):
    print("hello")
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )

    response = response.json()
    return {"message": "Authenticated", "access_token": response["access_token"]}