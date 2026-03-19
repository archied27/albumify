import sqlite3

"""
Initilaise the database to store album information from APIs
"""

def createAlbumDb(cur):
    # creates album table
    # stores spotify api details
    cur.execute("CREATE TABLE IF NOT EXISTS albums(\
        id TEXT PRIMARY KEY,\
        url TEXT,\
        album_popularity INTEGER,\
        album_name TEXT NOT NULL,\
        release_date DATETIME,\
        cover_path TEXT,\
        avg_track_duration REAL)")

def createArtistDb(cur):
    # creates artist table
    # stores spotify api artist details
    cur.execute("CREATE TABLE IF NOT EXISTS artists(\
        id TEXT PRIMARY KEY,\
        url TEXT,\
        artist_popularity INTEGER,\
        artist_name TEXT NOT NULL)")

def createGenreDb(cur):
    # creates genres table
    # stores genre names used for many to many relation with genres and albums
    cur.execute("CREATE TABLE IF NOT EXISTS genres(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        genre_name TEXT UNIQUE NOT NULL)")

def createArtistGenreDb(cur):
    # creates artist_genre table
    # used to link multiple genres to one artists
    cur.execute("CREATE TABLE IF NOT EXISTS artist_genres(\
        artist_id TEXT NOT NULL,\
        genre_id INTEGER NOT NULL,\
        PRIMARY KEY (artist_id, genre_id),\
        FOREIGN KEY(artist_id) REFERENCES artist(id) ON DELETE CASCADE,\
        FOREIGN KEY(genre_id) REFERENCES genres(id) ON DELETE CASCADE)")

def createAlbumArtistsDb(cur):
    # creates album_artists table
    # used to link albums with artists (many to many)
    cur.execute("CREATE TABLE IF NOT EXISTS album_artists(\
        album_id TEXT NOT NULL,\
        artist_id TEXT NOT NULL,\
        PRIMARY KEY (album_id, artist_id),\
        FOREIGN KEY(album_id) REFERENCES album(id) ON DELETE CASCADE,\
        FOREIGN KEY(artist_id) REFERENCES artist(id) ON DELETE CASCADE)")

def deleteAllTables(cur):
    cur.execute("DROP TABLE IF EXISTS artist_genres")
    cur.execute("DROP TABLE IF EXISTS album_artists")
    cur.execute("DROP TABLE IF EXISTS artists")
    cur.execute("DROP TABLE IF EXISTS genres")
    cur.execute("DROP TABLE IF EXISTS albums")

def createAllTables(cur):
    createAlbumDb(cur)
    createGenreDb(cur)
    createArtistDb(cur)
    createAlbumArtistsDb(cur)
    createArtistGenreDb(cur)

if __name__ == "__main__":
    con = sqlite3.connect('src/backend/app/db/albumify.db')
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    # delete and create all databases for a full reset
    deleteAllTables(cur)

    createAllTables(cur)

    con.commit()
    con.close()