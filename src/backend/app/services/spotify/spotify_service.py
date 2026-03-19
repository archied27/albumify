from app.services.spotify.auth import login, getToken
import requests
import sqlite3

BASE_URL = "https://api.spotify.com/v1"

def updateAlbumsDb(album):
    print(f"Adding {album['name']} by {album['artists'][0]['name']}")
    
    # updates the album table in database with albums info
    with sqlite3.connect("app/db/albumify.db") as conn:
        cur = conn.cursor()

        # artist = artistsGenreAndPop(album['artists'])

        # update albums table 
        cur.execute("INSERT INTO albums \
            (id, url, album_popularity, album_name, release_date, cover_path, avg_track_duration)\
            VALUES(?, ?, ?, ?, ?, ?, ?);",
            (album['id'], album['external_urls']['spotify'], album['popularity'], album['name'], 
            album['release_date'], album['images'][0]['url'], avgTrackDuration(album['tracks']['items'])) )

        #conn.commit()
        #conn.close()

def artistsGenreAndPop(artists):
    # takes an array of artists and returns their genres and avg popularity
    genres = []
    totalPop = 0

    for artist in artists:
        info = getArtistInfo(artist['id'])
        totalPop += info['popularity']
        genres = genres + info['genres'] # add all genres from all artists

    return {"genres": genres, "popularity":totalPop/len(artists)}

def avgTrackDuration(tracks):
    # takes an array of tracks and returns their average duration
    # in seconds
    totalSeconds = 0
    trackNo = 0
    for track in tracks:
        totalSeconds += track['duration_ms']
        trackNo += 1

    return totalSeconds/trackNo

def getSavedAlbums():
    # calls updateAlbumsDb with all albums in users library
    token = getToken()
    if token is not None:
        # set up requests url, headers and params
        url = BASE_URL + "/me/albums"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"limit": 50, "offset": 0}

        # loop until all users albums fetched
        while url:
            resp = requests.get(url, headers=headers, params=params)
            data = resp.json()
            url = data["next"] # set up next url to fetch (has params already set)

            for i in data["items"]:
                # for every album
                album = i['album']
                updateAlbumsDb(album)
            
            params = {}

        return {"message": "db updated"}

    else:
        return {"message": "not authenticated"}

def getArtistInfo(id):
    # returns spotify api artist info
    token = getToken()
    if token is not None:
        url = BASE_URL + f"/artists/{id}"
        headers = {"Authorization": f"Bearer {token}"}

        resp = requests.get(url, headers=headers)
        data = resp.json()

        return {"message": "success", "genres": data['genres'], "popularity": data['popularity']}
        
    else:
        return {"message": "not authenticated"}