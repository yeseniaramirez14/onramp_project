from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
import pandas as pd 
from d1_tables import *


# Load environment variables 
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
    "Rihanna",
    "Foo Fighters",
    "Natti Natasha",
    "Black Sabbath",
    "Van Halen",
    "Pink Floyd",
    "Britney Spears"
]


def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("No data available")
        return False 
    
    if df.isnull().values.any():
        num_nulls = df.isnull().sum().sum()
        raise Exception(f'{num_nulls} null values found')
    
    return True


#**** ETL ****# 


def insert_artists(conn):
    # Create artist table 
    create_artist_table(conn)

    # Loop through all my fav artists & pull the data via spotipy
    for artist in fav_artists:
        search_artist = sp.search(artist, limit=1, type="artist")
        access_artist_info = search_artist["artists"]["items"][0]

        # Save the data to dictionary
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

        # Constructing a DataFrame
        artist_df = pd.DataFrame(artist_info, index=[0])

        # Check if data is valid
        check_if_valid_data(artist_df)

        try:
            # Add to db
            artist_df.to_sql("artist", conn, index=False, if_exists='append')
        except:
            print(f'Artist, {artist_info["artist_name"]}, already exists in the database')

    print("****** ARTIST DATA INSERTED INTO TABLE ******")


def insert_albums(conn):
    # Create album table
    create_album_table(conn)
    
    # Select artist ids from db to use in search
    select_query = """
        SELECT artist_id
        FROM artist
    """
    cur = conn.cursor()
    cur.execute(select_query)

    # Fetchall() returns a list of tuples so I am converting that into a single list using list comprehension 
    artist_ids = [item[0] for item in cur.fetchall()]

    # Creating variables to check if album is already in db or a deluxe album
    in_db, deluxe = False, False

    # Looping through all the artist_ids
    for artist_id in artist_ids:

        # Pulling data via spotipy with an increased limit to get all the artists albums
        albums = sp.artist_albums(artist_id, album_type="album", limit=50, country="US")

        # Looping through all the albums available 
        for album in albums["items"]:
            # Inserting the data into a dictionary
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

            # Selecting current albums to check for duplicates
            select_albums_in_db = """
                SELECT album_name, artist_id
                FROM album;
            """
            cur.execute(select_albums_in_db)
            albums_in_db = cur.fetchall()

            # If no albums have been added to the db, then there is no data to compare it to so we need to add it 
            if len(albums_in_db) == 0:
                album_df = pd.DataFrame(album_info, index=[0])
                check_if_valid_data(album_df)
                album_df.to_sql("album", conn, index=False, if_exists='append')

            # Check to see if the current album already has a version inside the db
            for album_in_db in albums_in_db:
                if album["name"] in album_in_db and album["artists"][0]["id"] in album_in_db:
                    print(f'One version of {album["name"]} is already in the database')
                    in_db = True
            
            # Checking for deluxe albums 
            if "(Deluxe" in album["name"] or "Deluxe)" in album["name"] or "Deluxe Edition" in album["name"] or "Deluxe Version" in album["name"] or "Super Deluxe" in album["name"]:
                deluxe = True

            # Another way to search for deluxe albums, but it would be slower so I chose against it
            # deluxe_variations = ["(Deluxe", "Deluxe)", "Deluxe Edition", "Deluxe Version", "Super Deluxe"]
            # for variation in deluxe_variations:
            #     if variation in album["name"]:
            #         deluxe = True 
   
            # If the current album is not in_db and not a deluxe album, then we will add it to the db
            if in_db == False and deluxe == False:
                # Constructing a DataFrame & checking if valid data 
                album_df = pd.DataFrame(album_info, index=[0])
                check_if_valid_data(album_df)

                try:
                    album_df.to_sql("album", conn, index=False, if_exists='append')
                except:
                    print(f'Album, {album_info["album_name"]}, already exists in the database')

            # Reset our variables to false 
            in_db, deluxe = False, False
        
    print("****** ALBUM DATA INSERTED INTO TABLE ******")


def insert_tracks(conn):
    # Create track table 
    create_track_table(conn)

    # Select album ids
    select_query = """
        SELECT album_id
        FROM album
    """
    cur = conn.cursor()
    cur.execute(select_query)
    
    # Fetchall() returns a list of tuples so I am converting that into a single list using list comprehension 
    album_ids = [item[0] for item in cur.fetchall()]

    # Going through each album id and searching for it's tracks
    for album_id in album_ids:
        tracks = sp.album_tracks(album_id)

        # Adding data to dictionary 
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

            # Constructing a DataFrame and checking if the data is valid 
            track_df = pd.DataFrame(track_info, index=[0])
            check_if_valid_data(track_df)

            try: 
                # Insert into the database 
                track_df.to_sql("track", conn, index=False, if_exists='append')
            except:
                print(f'Track, {track_info["song_name"]}, already exists in the database')

    print("****** TRACK DATA INSERTED INTO TABLE ******")



def insert_features(conn):
    # Create a track_features table
    create_features_table(conn)

    # Select track ids 
    select_query = """
        SELECT track_id
        FROM track
    """
    cur = conn.cursor()
    cur.execute(select_query)

    # Fetchall() returns a list of tuples so I am converting that into a single list using list comprehension 
    track_ids = [item[0] for item in cur.fetchall()]

    # Getting the total number of tracks so we can do the least amount of API calls 
    # and search for a maximum of 100 tracks at a time 
    num_of_tracks = len(track_ids)
    
    starting_idx = 0
    stopping_idx = 100

    # Loop to make API calls with a maximum of 100 tracks at a time 
    for i in range((num_of_tracks // 100) + 1):
        features = sp.audio_features(track_ids[starting_idx:stopping_idx])

        # Add data to the dictionary 
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

            # Constructing a DataFrame and checking if valid data 
            feature_df = pd.DataFrame(feature_info, index=[0])
            check_if_valid_data(feature_df)

            try: 
                # Insert to the database 
                feature_df.to_sql("track_feature", conn, index=False, if_exists='append')
            except:
                print(f'Features for track {feature_info["track_id"]} already exists in the database')
        
        # Increase our indexes and move the window up 
        starting_idx = stopping_idx
        stopping_idx += 100

    print("****** FEATURE DATA INSERTED INTO TABLE ******")


def main():
    database = "spotify.db"

    # Create a database connection
    conn = create_connection(database)
    with conn:
        insert_artists(conn)
        insert_albums(conn)
        insert_tracks(conn)
        insert_features(conn)

if __name__ == '__main__':
    main()

