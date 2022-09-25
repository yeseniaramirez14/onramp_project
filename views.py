from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from tables import create_connection

load_dotenv()
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def top_songs_by_duration(conn):
    """
    Query top songs by artist in terms of duration_ms
    :param conn: the Connection object
    :return:
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS top_songs_by_duration;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_songs_by_duration
        AS
        SELECT
            t.song_name song_name,
            a.artist_name artist_name,
            MAX(t.duration_ms) duration_ms,
            strftime('%H:%M:%S', t.duration_ms/1000, 'unixepoch') minutes,
            alb.album_name album_name,
            a.genre genre
        FROM track t
        JOIN album alb
            ON alb.album_id = t.album_id
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        GROUP BY 2
        ORDER BY 3 DESC;    
    """
    cur.execute(create_view)
    conn.commit()

    # select_query = """
    #     SELECT *
    #     FROM top_songs_by_duration;
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


def top_songs_by_tempo(conn):
    """
    Query top songs by artists in terms of tempo
    :param conn: the Connection object
    :return:
    """   
    cur = conn.cursor()
    # cur.execute("DROP VIEW IF EXISTS top_songs_by_tempo;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_songs_by_tempo
        AS
        SELECT
            t.song_name song_name,
            a.artist_name artist_name,
            MAX(f.tempo) tempo,
            alb.album_name album_name,
            a.genre genre
        FROM track_feature f
        JOIN track t
            ON t.track_id = f.track_id
        JOIN album alb
            ON alb.album_id = t.album_id
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        GROUP BY 2
        ORDER BY 3 DESC;     
    """
    cur.execute(create_view)
    conn.commit()


def num_songs_albums_by_artist(conn):
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS num_songs_albums_by_artist;")
    create_view = """
        CREATE VIEW IF NOT EXISTS num_songs_albums_by_artist
        AS
        SELECT
            a.artist_name artist_name,
            COUNT(alb.album_name) total_albums,
            SUM(alb.total_tracks) total_songs
        FROM album alb
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        GROUP BY 1
        ORDER BY 2 DESC, 3 DESC;
    """
    cur.execute(create_view)
    conn.commit()
    
# SELECT
# 		a.artist_name artist_name,
# 		COUNT(alb.album_name) total_albums,
# 		SUM(alb.total_tracks) total_songs
# FROM album alb
# JOIN artist a
# 		ON a.artist_id = alb.artist_id 
# GROUP BY 1
# ORDER BY 2 DESC, 3 DESC;

        # SELECT 
        #     artist_name, 
        #     COUNT(album_name) num_albums,
        #     SUM(num_tracks) total_num_tracks
        # FROM 
        #     (SELECT
        #         a.artist_name artist_name,
        #         alb.album_name album_name,
        #         COUNT(t.song_name) num_tracks
        #     FROM track_feature f
        #     JOIN track t
        #         ON t.track_id = f.track_id
        #     JOIN album alb
        #         ON alb.album_id = t.album_id
        #     JOIN artist a
        #         ON a.artist_id = alb.artist_id 
        #     GROUP BY alb.album_id, a.artist_name
        #     ORDER BY 1, 2, 3) AS album_table
        # GROUP BY 1
        # ORDER BY 2 DESC, 3 DESC;



def main():
    database = "spotify.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("1. Query task by priority:")
        # select_task_by_priority(conn, 1)

        print("Query top songs by artist in terms of duration_ms")
        top_songs_by_duration(conn)

        print("Query top artists by the number of followers")
        top_artists_by_followers(conn)

        print("Query top songs by artist in terms of tempo")
        top_songs_by_tempo(conn)

        print("Query artists with the most albums and songs")
        num_songs_albums_by_artist(conn)


if __name__ == '__main__':
    main()
    