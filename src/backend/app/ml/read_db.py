"""
reads all relevant information from database ready for data preprocessing
"""

import sqlite3
import pandas as pd
import json
import os

# query to select per album
# # # album_id, album_name, release_date, album_popularity, avg_track_duration
# # # artist_names, avg_artist_pop, genres, album_tags, artist_tags
QUERY = """
SELECT
    a.id AS album_id,
    a.album_name,
    a.release_date,
    a.album_popularity,
    a.avg_track_duration,
    JSON_GROUP_ARRAY(DISTINCT ar.artist_name) AS artist_names,
    AVG(ar.artist_popularity) AS avg_artist_popularity,
    JSON_GROUP_ARRAY(DISTINCT g.genre_name) AS genres,
    JSON_GROUP_ARRAY(
        DISTINCT JSON_OBJECT('tag', t_album.name, 'weight', at_album.weight)
    ) AS album_tags,
    JSON_GROUP_ARRAY(
        DISTINCT JSON_OBJECT('tag', t_artist.name, 'weight', at_artist.weight)
    ) AS artist_tags
FROM albums a
LEFT JOIN album_artists aa ON a.id = aa.album_id
LEFT JOIN artists ar ON aa.artist_id = ar.id
LEFT JOIN artist_genres ag ON ar.id = ag.artist_id
LEFT JOIN genres g ON ag.genre_id = g.id
LEFT JOIN album_tags at_album ON a.id = at_album.album_id
LEFT JOIN tags t_album ON at_album.tag_id = t_album.id
LEFT JOIN artist_tags at_artist ON ar.id = at_artist.artist_id
LEFT JOIN tags t_artist ON at_artist.tag_id = t_artist.id
GROUP BY a.id
"""

def loadAlbumsDf(path):
    # returns dataframe of album info
    # ready for preprocessing

    # read sql info
    with sqlite3.connect(path) as con:
        df = pd.read_sql_query(QUERY, con)

    # set all features to correct formats
    df['artist_names'] = df['artist_names'].apply(json.loads)
    df['genres'] = df['genres'].apply(lambda x: [g for g in json.loads(x) if g is not None] or None)

    df['album_tags'] = df['album_tags'].apply(lambda x: parseJsonColumn(x, 'tag'))
    df['artist_tags'] = df['artist_tags'].apply(lambda x: parseJsonColumn(x, 'tag'))

    return df

def parseJsonColumn(val, nullCheckKey='tag'):
    # converts a string of json into actual json
    # also handles nulls
    parsed = json.loads(val)
    filtered = [item for item in parsed if item.get(nullCheckKey) is not None]
    return filtered if filtered else None
