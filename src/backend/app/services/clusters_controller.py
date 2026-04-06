"""
logic for fetching and renaming clusters
"""

import sqlite3

DB_PATH = "app/db/albumify.db"

def get_clusters():
    # returns each cluster with cluster name, album count
    data = {}

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT cluster_names.id, cluster_names.name, COUNT(DISTINCT albums.id)\
            FROM albums JOIN cluster_names ON (albums.cluster=cluster_names.id)\
            GROUP BY cluster_names.id, cluster_names.name")
        result = cur.fetchall()

    for cluster in result:
        data[cluster[0]] = {"name": cluster[1], "count": cluster[2]}

    return data

def cluster_albums(id):
    # returns all albums in a cluster
    data = {}

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT albums.id, albums.album_name, albums.release_date,\
            albums.cover_path, artists.artist_name, artists.id\
            FROM album_artists JOIN albums ON (album_artists.album_id = albums.id) JOIN artists ON (album_artists.artist_id = artists.id) \
            WHERE albums.cluster = ?\
            GROUP BY albums.id", [id,])
        result = cur.fetchall()

    for album in result:
        data[album[0]] = {"name": album[1], "release_date": album[2], "cover_path": album[3], "artist_name": album[4], "artist_id": album[5]}

    return data

def rename_cluster(id, name):
    # renames cluster with id, to name
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE cluster_names\
            SET name = ?\
            WHERE id = ?", [name, id])
    return {"message": "name updated"}
