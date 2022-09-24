from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sqlite3
from sqlite3 import Error
import pandas as pd 
from pprint import pprint

load_dotenv()
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None 
    try:
        conn = sqlite3.connect(db_file)
    except Error as error:
        print(error)
    
    return conn


# def select_artists(conn):
#     """
#     Query all rows in the tasks table
#     :param conn: the Connection object
#     :return:
#     """   
#     cur = conn.cursor()
#     test = """
#         SELECT *
#         FROM artist
#     """
#     cur.execute(test)

#     rows = cur.fetchall()
#     columns = cur.description

#     result = []
#     for value in rows:
#         tmp = {}
#         for (index,column) in enumerate(value):
#             tmp[columns[index][0]] = column
#         result.append(tmp)
#     pprint(result)


def top_songs_of_duration(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """   
    cur = conn.cursor()
    create_view = """
        CREATE VIEW IF NOT EXISTS top_songs_of_duration
        AS
        SELECT
            t.song_name song_name,
            a.artist_name artist_name,
            t.duration_ms duration_ms
        FROM track t
        JOIN album 
            ON album.album_id = t.album_id
        JOIN artist a
            ON a.artist_id = album.artist_id 
        ORDER BY 3 DESC;
    """
    cur.execute(create_view)

    select_query = """
        SELECT *
        FROM top_songs_of_duration;
    """
    cur.execute(select_query)

    rows = cur.fetchall()

    for row in rows:
        print(row)



# top_songs_of_duration()

def main():
    database = "spotify.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("1. Query task by priority:")
        # select_task_by_priority(conn, 1)

        print("Query all top songs by artist in terms of duration_ms")
        top_songs_of_duration(conn)


if __name__ == '__main__':
    main()
    