"""
logic for searching and getting album details
"""

import sqlite3
import json

DB_PATH = "app/db/albumify.db"

def get_all_albums():
    # returns all albums
    data = []

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT albums.id, albums.album_name, albums.release_date,\
            albums.cover_path, artists.artist_name, artists.id\
            FROM album_artists JOIN albums ON (album_artists.album_id = albums.id)\
            JOIN artists ON (album_artists.artist_id = artists.id)\
            GROUP BY albums.id\
            ORDER BY albums.release_date DESC")

        result = cur.fetchall()

    for album in result:
        data.append({"id": album[0], "name": album[1], "release_date": str(album[2])[:4], "cover_path": album[3], "artist_name": album[4], "artist_id": album[5]}) 
    
    return data

def get_album_info(id):
    # returns albums data
    data = {}

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                a.album_name,
                a.url,
                a.cover_path,
                cluster_names.name,
                a.release_date,
                a.album_popularity,
                JSON_GROUP_ARRAY(DISTINCT JSON_OBJECT('name', ar.artist_name, 'id', ar.id)) AS artists,
                JSON_GROUP_ARRAY(DISTINCT g.genre_name) AS genres,
                JSON_GROUP_ARRAY(
                    DISTINCT JSON_OBJECT('tag', t_album.name, 'weight', at_album.weight)
                    ORDER BY at_album.weight DESC
                ) AS album_tags
            FROM albums a
            LEFT JOIN album_artists aa ON a.id = aa.album_id
            LEFT JOIN artists ar ON aa.artist_id = ar.id
            LEFT JOIN artist_genres ag ON ar.id = ag.artist_id
            LEFT JOIN genres g ON ag.genre_id = g.id
            LEFT JOIN album_tags at_album ON a.id = at_album.album_id
            LEFT JOIN tags t_album ON at_album.tag_id = t_album.id
            LEFT JOIN cluster_names ON a.cluster = cluster_names.id
            WHERE a.id = ?
            GROUP BY a.id
            """, [id,])
        result = cur.fetchall()[0]
    
        data = {"name": result[0], "url": result[1], "cover_path": result[2], "cluster": result[3], "release_date": result[4],
            "popularity": result[5]}

        data["artists"] = json.loads(result[6])
        data["genres"] = json.loads(result[7])
        data["tags"] = json.loads(result[8])

    return data

def search_albums(query):
    # returns all albums with album name / artist name in search
    data = []

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT albums.id, albums.album_name, albums.release_date,
            albums.cover_path, artists.artist_name, artists.id
            FROM album_artists JOIN albums ON (album_artists.album_id = albums.id) JOIN artists ON (album_artists.artist_id = artists.id)
            WHERE (albums.album_name LIKE ?) OR (artists.artist_name LIKE ?)
            GROUP BY albums.id
            """, [f"%{query}%", f"%{query}%"])

        result = cur.fetchall()

        for album in result:
            data.append({"id": album[0], "name": album[1], "release_date": str(album[2])[:4], "cover_path": album[3], "artist_name": album[4], "artist_id": album[5]})

    return data