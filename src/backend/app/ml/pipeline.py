"""
carries out entire pipeline for ml
and adds to db
"""

import sqlite3
from app.ml.read_db import loadAlbumsDf
from app.ml.preprocess import preprocess
from app.ml.train_model import train_model

def add_clusters(db_path):
    df = loadAlbumsDf(db_path)
    df_scaled, df, scaler, reducer = preprocess(df)
    df_results, clusterer = train_model(df_scaled, df)
    
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        for index, row in df_results.iterrows():
            cur.execute("UPDATE albums\
                SET cluster = ?\
                WHERE id = ?", (row['cluster'], row['album_id']))

            cur.execute("INSERT INTO cluster_names\
                (id, name) VALUES (?, ?)\
                ON CONFLICT(id) DO UPDATE SET name=excluded.name", [row['cluster'], row['cluster']])
