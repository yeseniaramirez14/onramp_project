from tables import create_connection
from prettytable import from_db_cursor


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
            MAX(t.duration_ms) duration_ms,
            strftime('%H:%M:%S', t.duration_ms/1000, 'unixepoch') minutes,
            t.song_name song_name,
            a.artist_name artist_name,
            a.genre genre
        FROM track t
        JOIN album alb
            ON alb.album_id = t.album_id
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        GROUP BY 4
        ORDER BY 1 DESC, 2;    
    """
    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM top_songs_by_duration;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def top_artists_by_followers(conn):
    """
    Query top artists by the number of followers
    :param conn: the Connection object
    :return:
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS top_artists_by_followers;")
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

    select_query = """
        SELECT *
        FROM top_artists_by_followers;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def top_songs_by_tempo(conn):
    """
    Query top songs by artists in terms of tempo
    :param conn: the Connection object
    :return:
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS top_songs_by_tempo;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_songs_by_tempo
        AS
        SELECT
            printf('%.3f', MAX(f.tempo)) tempo,
            t.song_name song_name,
            a.artist_name artist_name,
            alb.album_name album_name
        FROM track_feature f
        JOIN track t
            ON t.track_id = f.track_id
        JOIN album alb
            ON alb.album_id = t.album_id
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        GROUP BY 3
        ORDER BY 1 DESC;     
    """
    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM top_songs_by_tempo;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


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
        ORDER BY 2 DESC, 3 DESC, 1;
    """
    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM num_songs_albums_by_artist;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def albums_released_in_90s(conn):
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS albums_released_in_90s;")
    create_view = """
        CREATE VIEW IF NOT EXISTS albums_released_in_90s
        AS
        SELECT
            strftime('%m-%d-%Y', alb.release_date) release_date,
            alb.album_name album_name,
            a.artist_name artist_name
        FROM album alb
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        WHERE strftime('%Y', alb.release_date) BETWEEN '1990' AND '2000'
        ORDER BY alb.release_date, 2, 3
    """
    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM albums_released_in_90s;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def main():
    database = "spotify.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Query top songs by artist in terms of duration_ms")
        top_songs_by_duration(conn)

        print("Query top artists by the number of followers")
        top_artists_by_followers(conn)

        print("Query top songs by artist in terms of tempo")
        top_songs_by_tempo(conn)

        print("Query artists with the most albums and songs")
        num_songs_albums_by_artist(conn)

        print("Query albums released before 2000")
        albums_released_in_90s(conn)

        print("Query number a songs an artist has with a danceability over 0.8")


if __name__ == '__main__':
    main()
    