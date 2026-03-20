"""
handles spotify api calls
and updating the database with spotify's features
"""

from app.services.spotify.auth import login, getToken
import requests
import sqlite3

BASE_URL = "https://api.spotify.com/v1"

def albumUpdateDb(album):
    # updates database with album information
    
    # updates the album table in database with albums info
    with sqlite3.connect("app/db/albumify.db") as conn:
        cur = conn.cursor()

        # update albums table 
        cur.execute("INSERT OR IGNORE INTO albums \
            (id, url, album_popularity, album_name, release_date, cover_path, avg_track_duration)\
            VALUES(?, ?, ?, ?, ?, ?, ?);",
            (album['id'], album['external_urls']['spotify'], album['popularity'], album['name'], 
            album['release_date'], album['images'][0]['url'], avgTrackDuration(album['tracks']['items'])) )

        # update all info for each artist on album
        artists = album['artists']
        for artist in artists:
            artistInfo = getArtistInfo(artist['id'], cur)
            if artistInfo['message'] == 'already in db':
                continue
            if artistInfo['message'] == "success":
                # update artists table
                cur.execute("INSERT OR IGNORE INTO artists \
                    (id, url, artist_popularity, artist_name)\
                    VALUES(?, ?, ?, ?);",
                    (artist['id'], artistInfo['url'], artistInfo['popularity'], artistInfo['name']))
                
                # link artist(s) to album
                cur.execute("INSERT OR IGNORE INTO album_artists\
                    (album_id, artist_id)\
                    VALUES(?, ?);", (album['id'], artist['id']))
                
                for genre in artistInfo['genres']:
                    # add genre to genre table if not already there
                    cur.execute("INSERT OR IGNORE INTO genres\
                    (genre_name) VALUES(?)", (genre,))

                    # link genre to artist
                    cur.execute("SELECT id FROM genres WHERE genre_name = ?", (genre,))
                    genreId = cur.fetchone()[0] # select genre's id
                    cur.execute("INSERT OR IGNORE INTO artist_genres\
                    (artist_id, genre_id) VALUES(?, ?)", (artist['id'], genreId))

            else:
                print(f"error fetching {artist['name']}")

def avgTrackDuration(tracks):
    # takes an array of tracks and returns their average duration
    # in seconds
    totalSeconds = 0
    trackNo = 0
    for track in tracks:
        totalSeconds += track['duration_ms']
        trackNo += 1

    return totalSeconds/trackNo

def updateDb():
    # calls updateDb with all albums in users library
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
                albumUpdateDb(album)
            
            params = {}

        return {"message": "db updated"}

    else:
        return {"message": "not authenticated"}

def getArtistInfo(id, cur):
    # returns spotify api artist info
    
    # if already in database
    cur.execute("SELECT 1 FROM artists WHERE (id=?)", (id,))
    if cur.fetchone() is not None:
        return {"message": "already in db"}

    # if not already in database
    token = getToken()
    if token is not None:
        url = BASE_URL + f"/artists/{id}"
        headers = {"Authorization": f"Bearer {token}"}

        resp = requests.get(url, headers=headers)
        data = resp.json()

        return {"message": "success", "genres": data['genres'], "popularity": data['popularity'], "name": data['name'], "url": data['external_urls']['spotify']}
        
    else:
        return {"message": "not authenticated"}