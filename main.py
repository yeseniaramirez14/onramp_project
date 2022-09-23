from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sqlite3
from pprint import pprint
import pandas as pd 

load_dotenv()
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

conn = sqlite3.connect("spotify.db")
cursor = conn.cursor()

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

        try:
            artist_df.to_sql("artist", conn, index=False, if_exists='append')
            print("Added data to the database")
        except:
            print(f'Artist {artist_info["artist_name"]} already exists in the database')

    conn.commit()
    print("****** ARTIST IS DONE ******")


def get_albums():
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

    # fetchall() returns a list of tuples so I am converting that into a single list using list comprehension 
    artist_ids = [item[0] for item in cursor.fetchall()]

    for artist_id in artist_ids:
        albums = sp.artist_albums(artist_id, album_type="album", country="US")
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
                print(f'Album {album_info["album_name"]} already exists in the database')
        
    conn.commit()
    print("****** ALBUM IS DONE ******")



def get_tracks():
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
    album_ids = [item[0] for item in cursor.fetchall()]

    for album_id in album_ids:
        tracks = sp.album_tracks(album_id)
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
                print(f'Track {track_info["song_name"]} already exists in the database')

    conn.commit()

    print("****** TRACK IS DONE ******")



def get_features():
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
        )
    """
    cursor.execute(feature_table)

    select_query = """
        SELECT track_id
        FROM track
    """
    cursor.execute(select_query)
    track_ids = [item[0] for item in cursor.fetchall()]
    num_of_tracks = len(track_ids)
    
    starting_idx = 0
    stopping_idx = 100

    for i in range(num_of_tracks // 100):
        features = sp.audio_features(track_ids[starting_idx:stopping_idx])
        for feature in features:
            feature_info = {
                "track_id": feature["id"],
                "danceability": feature["danceability"],
                "energy": feature["energy"],
                "instrumentalness": feature["instrumentalness"],
                "liveness": feature["liveness"],
                "loudness": feature["loudness"],
                "speechiness": feature["speechiness"],
                "tempo": feature["tempo"],
                "type": feature["type"],
                "valence": feature["valence"],
                "song_uri": feature["uri"],
            }

            feature_df = pd.DataFrame(feature_info, index=[0])

            try: 
                feature_df.to_sql("track_feature", conn, index=False, if_exists='append')
                print("Added data to the database")
            except:
                print(f'Features for track {feature_info["track_id"]} already exists in the database')
        
        starting_idx = stopping_idx
        stopping_idx += 100

    conn.commit()

    print("****** FEATURES IS DONE ******")



get_artists()
get_albums()
get_tracks()
get_features()

conn.close()


