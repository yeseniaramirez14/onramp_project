from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sqlite3
import sys
from pprint import pprint
import pandas as pd 

load_dotenv
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


fav_artists = [
    "Drake",
    "Becky G",
    "Jack Harlow",
    "Karol G",
    "Bad Bunny",
    "J Balvin",
    "Grupo Firme",
    "Queen",
    "Lynyrd Skynyrd",
    "Nirvana",
    "Led Zeppelin"
]


#**** INGESTION && TRANSFORMATION ****#
def get_artists():
    conn = sqlite3.connect("spotify.db")
    cursor = conn.cursor()

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
        )
    """
    cursor.execute(artist_table)

    for artist in fav_artists:
        search_artist = sp.search(artist, limit=1, type="artist")
        access_artist_info = search_artist["artists"]["items"][0]
    
        artist_info = {
            "artist_id": access_artist_info["id"],
            "artist_name": access_artist_info["name"],
            "external_url": access_artist_info["external_urls"]["spotify"],
            "genre": access_artist_info["genres"][0],
            "image_url": access_artist_info["images"][0]["url"],
            "followers": access_artist_info["followers"]["total"],
            "popularity": access_artist_info["popularity"],
            "type": access_artist_info["type"],
            "artist_uri": access_artist_info["uri"]
        }

        artist_df = pd.DataFrame(artist_info, index=[0])
        # print("artist_df:")
        # pprint(artist_df)

        try:
            artist_df.to_sql("artist", conn, index=False, if_exists='append')
            print("Added data to the database")
        except:
            print("Data already exists in the database")

    conn.close()


def get_albums():
    conn = sqlite3.connect("spotify.db")
    cursor = conn.cursor()
    
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
        )
    """
    cursor.execute(album_table)

    select_query = """
        SELECT artist_id 
        FROM artist
    """
    cursor.execute(select_query)
    artist_ids = cursor.fetchall()

    for artist_id in artist_ids:
        albums = sp.artist_albums(artist_id[0], album_type="album", country="US")
        for album in albums["items"]:
            album_info = {
                "album_id": album["id"],
                "album_name": album["name"],
                "external_url": album["external_urls"]["spotify"],
                "image_url": album["images"][0]["url"],
                "release_date": album["release_date"],
                "total_tracks": album["total_tracks"],
                "type": album["type"],
                "album_uri": album["uri"],
                "artist_id": album["artists"][0]["id"],
            }

            album_df = pd.DataFrame(album_info, index=[0])

            try:
                album_df.to_sql("album", conn, index=False, if_exists='append')
                print("Added data to the database")
            except:
                print("Data already exists in the database")
        
    conn.close()


def get_tracks():
    conn = sqlite3.connect("spotify.db")
    cursor = conn.cursor()

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
        )
    """
    cursor.execute(track_table)

    select_query = """
        SELECT album_id
        FROM album
    """
    cursor.execute(select_query)
    album_ids = cursor.fetchall()

    for album_id in album_ids:
        tracks = sp.album_tracks(album_id[0])
        for track in tracks["items"]:
            track_info = {
                "track_id": track["id"],
                "song_name": track["name"],
                "external_url": track["external_urls"]["spotify"],
                "duration_ms": track["duration_ms"],
                "explicit": track["explicit"],
                "disc_number": track["disc_number"],
                "type": track["type"],
                "song_uri": track["uri"],
                "album_id": album_id[0],
            }

            track_df = pd.DataFrame(track_info, index=[0])

            try: 
                track_df.to_sql("track", conn, index=False, if_exists='append')
                print("Added data to the database")
            except:
                print("Data already exists in the database")

    conn.close()

def get_features():
    tracks = []
    features = sp.audio_features(tracks)

# get_artists()
# get_albums()
# get_tracks()
get_features()



