import sqlite3
from sqlite3 import Error


# Create a connection and cursor object
try:
    conn = sqlite3.connect("spotify.db")
    cursor = conn.cursor()
    print("Database created and successfully connected to SQLite")
except Error as error:
    print("Error while connecting to SQLite:", error)


#**** CREATE ALL TABLES ****# 
def create_artist_table():
    artist_table = """
        CREATE TABLE IF NOT EXISTS artist(
            artist_id VARCHAR(50) PRIMARY KEY,
            artist_name VARCHAR(255),
            external_url VARCHAR(100),
            genre VARCHAR(100),
            image_url VARCHAR(100),
            followers INT,
            popularity INT,
            type VARCHAR(50),
            artist_uri VARCHAR(100)
        );
    """
    cursor.execute(artist_table)
    conn.commit()
    print("****** ARTIST TABLE CREATED ******")


def create_album_table():
    album_table = """
        CREATE TABLE IF NOT EXISTS album(
            album_id VARCHAR(50) PRIMARY KEY,
            album_name VARCHAR(255),
            external_url VARCHAR(100),
            image_url VARCHAR(100),
            release_date date,
            total_tracks INT,
            type VARCHAR(50),
            album_uri VARCHAR(100),
            artist_id VARCHAR(50),
            FOREIGN KEY(artist_id) REFERENCES artist(artist_id)
        );
    """
    cursor.execute(album_table)
    conn.commit()
    print("****** ALBUM TABLE CREATED ******")


def create_track_table():
    track_table = """
        CREATE TABLE IF NOT EXISTS track(
            track_id VARCHAR(50) PRIMARY KEY,
            song_name VARCHAR(255),
            external_url VARCHAR(100),
            duration_ms INT,
            explicit BOOLEAN,
            disc_number INT,
            type VARCHAR(50),
            song_uri VARCHAR(100),
            album_id VARCHAR(50),
            FOREIGN KEY(album_id) REFERENCES album(album_id)
        );
    """
    cursor.execute(track_table)
    conn.commit()
    print("****** TRACK TABLE CREATED ******")


def create_features_table():
    feature_table = """
        CREATE TABLE IF NOT EXISTS track_feature(
            track_id VARCHAR(50) PRIMARY KEY,
            danceability DOUBLE,
            energy DOUBLE,
            instrumentalness DOUBLE,
            liveness DOUBLE,
            loudness DOUBLE,
            speechiness DOUBLE,
            tempo DOUBLE,
            type VARCHAR(50),
            valence DOUBLE,
            song_uri VARCHAR(100),
            FOREIGN KEY(track_id) REFERENCES track(track_id)
        );
    """
    cursor.execute(feature_table)
    conn.commit()
    print("****** FEATURES TABLE CREATED ******")


create_artist_table()
create_album_table()
create_track_table()
create_features_table()

conn.close()