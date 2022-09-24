from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from tables import create_connection

load_dotenv()
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def top_songs_of_duration(conn):
    """
    Query top songs by artist in terms of duration_ms
    :param conn: the Connection object
    :return:
    """   
    cur = conn.cursor()
    # cur.execute("DROP VIEW IF EXISTS top_songs_of_duration;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_songs_of_duration
        AS
        SELECT
			t.duration_ms duration_ms,
			strftime('%H:%M:%S', t.duration_ms/1000, 'unixepoch') minutes,
            t.song_name song_name,
            a.artist_name artist_name,
			alb.album_name album_name,
			a.genre genre
        FROM track t
        JOIN album alb
            ON alb.album_id = t.album_id
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        ORDER BY 1 DESC;     
    """
    cur.execute(create_view)
    conn.commit()

    # select_query = """
    #     SELECT *
    #     FROM top_songs_of_duration;
    # """
    # cur.execute(select_query)

    # rows = cur.fetchall()

    # for row in rows:
    #     print(row)


def top_artists_by_followers(conn):
    """
    Query top artists by the number of followers
    :param conn: the Connection object
    :return:
    """   
    cur = conn.cursor()
    # cur.execute("DROP VIEW IF EXISTS top_artists_by_followers;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_artists_by_followers
        AS
        SELECT
			a.followers num_followers,
			a.popularity popularity,
			a.artist_name artist_name,
			a.genre genre,
			COUNT(*) num_albums,
			STRFTIME('%m-%d-%Y', MAX(alb.release_date)) latest_album_release_date
        FROM artist a
        JOIN album alb
            ON alb.artist_id = a.artist_id
		GROUP BY 3
        ORDER BY 1 DESC;     
    """
    cur.execute(create_view)
    conn.commit()


def main():
    database = "spotify.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("1. Query task by priority:")
        # select_task_by_priority(conn, 1)

        print("Query top songs by artist in terms of duration_ms")
        top_songs_of_duration(conn)

        print("Query top artists by the number of followers")
        top_artists_by_followers(conn)


if __name__ == '__main__':
    main()
    