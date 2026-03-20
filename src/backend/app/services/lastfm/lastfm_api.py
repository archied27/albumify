"""
handle lastfm api calls
and updating lastfm related database (tags)
"""
import requests
import sqlite3
import dotenv
import os
import json
import re

dotenv.load_dotenv()
API_KEY = os.getenv("LAST_FM_KEY")

BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def albumUpdateDb(album, artist, albumId, cur):
    # takes in an album name and corresponding artist 
    # and albumId from db and cur to db
    # fetches tags and updates database with them

    album = cleanAlbumName(album)
    tags = getAlbumTags(album, artist)

    for tag in tags:
        # add to tags table if not already there
        cur.execute("INSERT OR IGNORE INTO tags\
            (name) VALUES (?);", (tag['name'],))
        
        cur.execute("SELECT id FROM tags WHERE name=?", (tag['name'],))
        tagId = cur.fetchone()[0]
        # link to album
        cur.execute("INSERT OR IGNORE INTO album_tags\
            (album_id, tag_id, weight) VALUES (?, ?, ?)", (albumId, tagId, tag['weight']))
        
def artistUpdateDb(artist, artistId, cur):
    # takes in an artist name and corresponding id from db
    # and cur to db
    # fetches tags and updates database with them

    tags = getArtistTags(artist)

    for tag in tags:
        # add to tags table if not already there
        cur.execute("INSERT OR IGNORE INTO tags\
            (name) VALUES (?);", (tag['name'],))

        cur.execute("SELECT id FROM tags WHERE name=?", (tag['name'],))
        tagId = cur.fetchone()[0]
        # link to artist
        cur.execute("INSERT OR IGNORE INTO artist_tags\
            (artist_id, tag_id, weight) VALUES (?, ?, ?)", (artistId, tagId, tag['weight']))
        
def updateDb():
    # fetches and updates db with all album and artist tags
    # which are already in db
    with sqlite3.connect("src/backend/app/db/albumify.db") as conn:
        cur = conn.cursor()
        # get all album id's, names, and artist names
        cur.execute("SELECT albums.id, albums.album_name, artists.artist_name\
            FROM albums, artists, album_artists\
            WHERE (albums.id = album_artists.album_id) AND (artists.id = album_artists.artist_id)\
            GROUP BY albums.id")
        albums = cur.fetchall()
        # update db with all album tags
        for album in albums:
            print(f"Adding {album[1]}")
            albumUpdateDb(album[1], album[2], album[0], cur)

        # get all artist ids and names
        cur.execute("SELECT id, artist_name\
            FROM artists")
        artists = cur.fetchall()
        # update db with all artists tags
        for artist in artists:
            print(f"Adding {artist[1]}")
            artistUpdateDb(artist[1], artist[0], cur)
    return {"message": "db updated"}

        



def cleanAlbumName(album):
    # returns a 'clean' album name
    # i.e with no (2015 Remaster), etc
    cleaned = re.sub(r'[\(\[][^\)\]]*[\)\]]', '', album)
    return cleaned.strip()

def getAlbumTags(album, artist):
    # returns tags for album
    # takes in album and artist name
    tags = []

    params = {
        "method": "album.getTopTags",
        "artist": artist,
        "album": album,
        "api_key": API_KEY,
        "format": "json"
    }

    resp = requests.get(BASE_URL, params=params)
    data = resp.json()

    # clean data to only show tag name and corresponding weight
    if resp.status_code == 200:
        tags = data['toptags']['tag']
        tags = [{"name": tag['name'].lower(), "weight": tag['count']} for tag in tags]
    return tags

def getArtistTags(artist):
    # returns tags for artist
    # takes in artist name
    tags = []

    params = {
        "method": "artist.getTopTags",
        "artist": artist,
        "api_key": API_KEY,
        "format": "json"
    }

    resp = requests.get(BASE_URL, params=params)
    data = resp.json()

    # clean data to only show tag name and corresponding weight
    if resp.status_code == 200:
        tags = data['toptags']['tag']
        tags = [{"name": tag['name'].lower(), "weight": tag['count']} for tag in tags]
    return tags

updateDb()