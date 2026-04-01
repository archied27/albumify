"""
preprocess the dataframe ready for model
returns df ready for model, original model for reference, and the scaler used and reducer used
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
import umap
import math

def preprocess(df):
    # release year
    df['release_year'] = df['release_date'].apply(parseReleaseYear)
    df.drop(columns=['release_date'], inplace=True)

    # multi hot encodings
    # genres
    # then multi-hot encode genres
    mlbGenres = MultiLabelBinarizer()
    genreMatrix = mlbGenres.fit_transform(df['genres'].apply(lambda x: x if x else []))
    genre_df = pd.DataFrame(genreMatrix, columns=[f"genre_{g}" for g in mlbGenres.classes_])

    # then tags
    all_album_tags = set(t['tag'] for tags in df['album_tags'].dropna() for t in tags)
    album_tag_df = pd.DataFrame(df['album_tags'].apply(lambda x: buildTagVector(x, all_album_tags)).tolist())
    all_artist_tags = set(t['tag'] for tags in df['artist_tags'].dropna() for t in tags)
    artist_tag_df = pd.DataFrame(df['artist_tags'].apply(lambda x: buildTagVector(x, all_artist_tags)).tolist())

    # build ml df
    df_ml = df.drop(columns=['album_id', 'album_name', 'artist_names', 
                            'genres', 'album_tags', 'artist_tags'])

    # combine with encoded columns
    df_ml = pd.concat([df_ml, genre_df, artist_tag_df, album_tag_df], axis=1)

    # add decade feature
    df['decade'] = (df['release_year'] // 10 * 10).astype(int)
    decade_dummies = pd.get_dummies(df['decade'], prefix='decade')
    df_ml = pd.concat([df_ml, decade_dummies], axis=1)

    # scale
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_ml), columns=df_ml.columns)

    # reduce
    reducer = umap.UMAP(n_neighbors=int(math.sqrt(len(df_scaled))), n_components=10, min_dist=0, metric='cosine')
    df_scaled = reducer.fit_transform(df_scaled)

    return df_scaled, df, scaler, reducer

def parseReleaseYear(date):
    if pd.isna(date):
        return None
    parsed = pd.to_datetime(date, errors='coerce')
    if pd.notna(parsed):
        return parsed.year
    return int(str(date)[:4])

def buildTagVector(tags, all_tags):
    vec = {f"atag_{t}": 0 for t in all_tags}
    if tags:
        for t in tags:
            vec[f"atag_{t['tag']}"] = t['weight']
    return vec
