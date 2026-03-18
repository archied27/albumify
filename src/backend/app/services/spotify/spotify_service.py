from app.services.spotify.auth import login, getToken
import requests

BASE_URL = "https://api.spotify.com/v1"

def getSavedAlbums():
    token = getToken()
    if token is not None:
        # get users albums
        url = BASE_URL + "/me/albums"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"limit": 50, "offset": 0}

        savedAlbums = []

        while url:
            resp = requests.get(url, headers=headers, params=params)
            data = resp.json()
            url = data["next"]
            for i in data["items"]:
                savedAlbums.append(i['album']['name'])
            
            params = {}

        return savedAlbums

    else:
        return {"error": "authentication failed"}