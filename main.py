from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sqlite3
from sqlite3 import Error
from pprint import pprint
import pandas as pd 
from tables import create_connection, create_album_table, create_artist_table, create_features_table, create_track_table

load_dotenv()
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
    "Led Zeppelin",
    "Billie Eilish",
    "J. Cole",
    "The Beatles",
    "Rihanna",
    "Foo Fighters",
    "Natti Natasha"
]


def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("No data available")
        return False 
    
    if df.isnull().values.any():
        num_nulls = df.isnull().sum().sum()
        raise Exception(f'{num_nulls} null values found')
    
    return True

#**** INGESTION && TRANSFORMATION ****# 
def insert_artists(conn):
    create_artist_table(conn)
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
        check_if_valid_data(artist_df)

        try:
            artist_df.to_sql("artist", conn, index=False, if_exists='append')
        except:
            print(f'Artist, {artist_info["artist_name"]}, already exists in the database')

    conn.commit()
    print("****** ARTIST DATA INSERTED INTO TABLE ******")


def insert_albums(conn):
    create_album_table(conn)
    
    select_query = """
        SELECT artist_id 
        FROM artist
    """
    cur = conn.cursor()
    cur.execute(select_query)

    # fetchall() returns a list of tuples so I am converting that into a single list using list comprehension 
    artist_ids = [item[0] for item in cur.fetchall()]

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
            check_if_valid_data(album_df)

            try:
                album_df.to_sql("album", conn, index=False, if_exists='append')
            except:
                print(f'Album, {album_info["album_name"]}, already exists in the database')
        
    conn.commit()
    print("****** ALBUM DATA INSERTED INTO TABLE ******")



def insert_tracks(conn):
    create_track_table(conn)
    select_query = """
        SELECT album_id
        FROM album
    """
    cur = conn.cursor()
    cur.execute(select_query)
    album_ids = [item[0] for item in cur.fetchall()]

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
                "album_id": album_id,
            }

            track_df = pd.DataFrame(track_info, index=[0])
            check_if_valid_data(track_df)

            try: 
                track_df.to_sql("track", conn, index=False, if_exists='append')
            except:
                print(f'Track, {track_info["song_name"]}, already exists in the database')

    conn.commit()

    print("****** TRACK DATA INSERTED INTO TABLE ******")



def insert_features(conn):
    create_features_table(conn)

    select_query = """
        SELECT track_id
        FROM track
    """
    cur = conn.cursor()
    cur.execute(select_query)
    track_ids = [item[0] for item in cur.fetchall()]
    num_of_tracks = len(track_ids)
    
    starting_idx = 0
    stopping_idx = 100

    for i in range((num_of_tracks // 100) + 1):
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
            check_if_valid_data(feature_df)

            try: 
                feature_df.to_sql("track_feature", conn, index=False, if_exists='append')
            except:
                print(f'Features for track {feature_info["track_id"]} already exists in the database')
        
        starting_idx = stopping_idx
        stopping_idx += 100

    conn.commit()
    print("****** FEATURE DATA INSERTED INTO TABLE ******")

def main():
    database = "spotify.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        insert_artists(conn)
        insert_albums(conn)
        insert_tracks(conn)
        insert_features(conn)

if __name__ == '__main__':
    main()

