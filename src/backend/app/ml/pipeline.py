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

            cur.execute("INSERT OR IGNORE INTO cluster_names\
                (id, name) VALUES (?, ?)", [row['cluster'], row['cluster']])
