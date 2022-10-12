from d1_tables import create_connection
from prettytable import from_db_cursor


def top_10_songs_by_duration_per_artist(conn):
    """
    Query top 10 songs by artist in terms of duration_ms
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS top_10_songs_by_duration_per_artist;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_10_songs_by_duration_per_artist
        AS
        SELECT artist_name, song_name, duration_ms, minutes
        FROM (
            SELECT
                a.artist_name,
                t.song_name,
                t.duration_ms,
                strftime('%H:%M:%S', t.duration_ms/1000, 'unixepoch') minutes,
                row_number() over (
                    PARTITION BY a.artist_name 
                    ORDER BY a.artist_name, t.duration_ms DESC
                ) as longest_duration
            FROM track t
            JOIN album alb
                ON alb.album_id = t.album_id
            JOIN artist a
                ON a.artist_id = alb.artist_id) duration_ranks
        WHERE longest_duration <= 10;
    """
    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM top_10_songs_by_duration_per_artist;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def top_20_artists_by_followers(conn):
    """
    Query top 20 artists in the db by the number of followers
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS top_20_artists_by_followers;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_20_artists_by_followers
        AS
        SELECT
			a.artist_name,
			a.followers,
			a.popularity,
			a.genre,
			COUNT(*) num_albums,
			STRFTIME('%m-%d-%Y', MAX(alb.release_date)) latest_album_release_date
        FROM artist a
        JOIN album alb
            ON alb.artist_id = a.artist_id
		GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 20;   
    """
    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM top_20_artists_by_followers;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def top_10_songs_by_tempo_per_artist(conn):
    """
    Query top 10 songs by artists in terms of tempo
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS top_10_songs_by_tempo_per_artist;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_10_songs_by_tempo_per_artist
        AS
        SELECT artist_name, song_name, tempo, album_name
		FROM (
			SELECT
				a.artist_name,
				t.song_name,
				printf('%.3f', f.tempo) tempo,
				alb.album_name,
				row_number() over (
					PARTITION BY a.artist_name
					ORDER BY a.artist_name, f.tempo DESC
				) as highest_tempo
			FROM track_feature f
			JOIN track t
				ON t.track_id = f.track_id
			JOIN album alb
				ON alb.album_id = t.album_id
			JOIN artist a
				ON a.artist_id = alb.artist_id) tempo_ranks
		WHERE highest_tempo <= 10;
    """
    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM top_10_songs_by_tempo_per_artist;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def num_songs_albums_by_artist(conn):
    """
    Query how many songs and albums each artist has 
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS num_songs_albums_by_artist;")
    create_view = """
        CREATE VIEW IF NOT EXISTS num_songs_albums_by_artist
        AS
        SELECT
            a.artist_name,
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
    """
    Query the albums that were released in the 1990's
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS albums_released_in_90s;")
    create_view = """
        CREATE VIEW IF NOT EXISTS albums_released_in_90s
        AS
        SELECT
            strftime('%m-%d-%Y', alb.release_date) release_date,
            alb.album_name,
            a.artist_name
        FROM album alb
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        WHERE strftime('%Y', alb.release_date) BETWEEN '1990' AND '2000'
        ORDER BY alb.release_date, 2, 3;
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


def top_20_songs_by_danceability(conn):
    """
    Query top 20 songs by danceability 
    :param conn: the Connection object
    :return:
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS top_20_songs_by_danceability;")
    create_view = """
        CREATE VIEW IF NOT EXISTS top_20_songs_by_danceability
        AS
        SELECT
		    a.artist_name,
            t.song_name,
            printf('%.3f', f.danceability) danceability
        FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f
            ON f.track_id = t.track_id
		WHERE f.danceability >= 0.80
        ORDER BY 3 DESC
		LIMIT 20;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM top_20_songs_by_danceability;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def avg_energy_of_artist(conn):
    """
    Query average energy level of each artist 
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS avg_energy_of_artist;")
    create_view = """
        CREATE VIEW IF NOT EXISTS avg_energy_of_artist
        AS
        SELECT
            a.artist_name,
			a.genre,
            printf('%.3f', AVG(f.energy)) energy
        FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f
            ON f.track_id = t.track_id
		GROUP BY 1
        ORDER BY 3 DESC;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM avg_energy_of_artist;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def artists_w_atleast_20_albums(conn):
    """
    Query artists with at least 20 albums
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS artists_w_atleast_20_albums;")
    create_view = """
        CREATE VIEW IF NOT EXISTS artists_w_atleast_20_albums
        AS
        SELECT
            a.artist_name,
            COUNT(alb.album_name) total_albums
		FROM album alb
        JOIN artist a
            ON a.artist_id = alb.artist_id 
        GROUP BY 1
		HAVING COUNT(alb.album_name) > 20
        ORDER BY 2 DESC, 1;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM artists_w_atleast_20_albums;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def avg_audio_features_by_genre(conn):
    """
    Query average audio features by genre
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS avg_audio_features_by_genre;")
    create_view = """
        CREATE VIEW IF NOT EXISTS avg_audio_features_by_genre
        AS
        SELECT
            a.genre,
			printf('%.1f', AVG(a.popularity)) popularity,
            printf('%.3f', AVG(f.danceability)) danceability,
            printf('%.3f', AVG(f.energy)) energy,
            printf('%.3f', AVG(f.instrumentalness)) instrumentalness, 
            printf('%.3f', AVG(f.liveness)) liveness,
            printf('%.3f', AVG(f.loudness)) loudness,
            printf('%.3f', AVG(f.speechiness)) speechiness,
            printf('%.3f', AVG(f.tempo)) tempo,
            printf('%.3f', AVG(f.valence)) valence 
        FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id 
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f 
            ON f.track_id = t.track_id
        GROUP BY 1
        ORDER BY 2 DESC;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM avg_audio_features_by_genre;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def loudness_energy_by_genre(conn):
    """
    Query audio features by genre
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS loudness_energy_by_genre;")
    create_view = """
        CREATE VIEW IF NOT EXISTS loudness_energy_by_genre
        AS
        SELECT
            a.genre,
            printf('%.3f', f.energy) energy,
			printf('%.3f', f.loudness) loudness
        FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id 
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f 
            ON f.track_id = t.track_id
        ORDER BY 1;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM loudness_energy_by_genre;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def avg_audio_features_by_artist(conn):
    """
    Query average audio features by artist
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS avg_audio_features_by_artist;")
    create_view = """
        CREATE VIEW IF NOT EXISTS avg_audio_features_by_artist
        AS
        SELECT
            a.artist_name Artist,
            printf('%.3f', AVG(f.danceability)) Danceability,
            printf('%.3f', AVG(f.energy)) Energy,
            printf('%.3f', AVG(f.tempo)) Tempo,
            printf('%.3f', AVG(f.speechiness)) Speechiness,
            printf('%.3f', AVG(f.instrumentalness)) Instrumentalness, 
            printf('%.3f', AVG(f.valence)) Valence 
        FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id 
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f 
            ON f.track_id = t.track_id
        GROUP BY a.artist_id
        ORDER BY 1;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM avg_audio_features_by_artist;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def audio_features_correlations(conn):
    """
    Query average audio features by artist
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS audio_features_correlations;")
    create_view = """
        CREATE VIEW IF NOT EXISTS audio_features_correlations
        AS
        SELECT
            printf('%.3f', f.danceability) Danceability,
            printf('%.3f', f.energy) Energy,
            printf('%.3f', f.tempo) Tempo,
            printf('%.3f', f.speechiness) Speechiness,
            printf('%.3f', f.instrumentalness) Instrumentalness, 
            printf('%.3f', f.valence) Valence 
        FROM track_feature f
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM audio_features_correlations;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def audio_features_for_album(conn):
    """
    Query audio features for Jack Harlow's album, 
    Come Home The Kids Miss You
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS audio_features_for_album;")
    create_view = """
        CREATE VIEW IF NOT EXISTS audio_features_for_album
        AS
        SELECT
			t.song_name,
            printf('%.3f', f.danceability) danceability,
            printf('%.3f', f.energy) energy,
            printf('%.3f', f.instrumentalness) instrumentalness, 
            printf('%.3f', f.liveness) liveness,
            printf('%.3f', f.loudness) loudness,
            printf('%.3f', f.speechiness) speechiness,
            printf('%.3f', f.tempo) tempo,
            printf('%.3f', f.valence) valence 
        FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id 
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f 
            ON f.track_id = t.track_id
		WHERE alb.album_id = '2eE8BVirX9VF8Di9hD90iw'
        ORDER BY 1;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM audio_features_for_album;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def popularity_by_artists_in_genre(conn):
    """
    Query popularity by artists
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS popularity_by_artists_in_genre;")
    create_view = """
        CREATE VIEW IF NOT EXISTS popularity_by_artists_in_genre
        AS
        SELECT
			a.artist_name,
			a.genre,
            a.popularity
        FROM artist a
        ORDER BY 3 DESC;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM popularity_by_artists_in_genre;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def tempos_by_genre(conn):
    """
    Query tempos of songs by genre 
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS tempos_by_genre;")
    create_view = """
        CREATE VIEW IF NOT EXISTS tempos_by_genre
        AS
        SELECT
            a.genre,
			CAST(f.tempo AS INT) tempo,
            a.artist_name,
			t.song_name
		FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id 
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f 
            ON f.track_id = t.track_id
        WHERE f.tempo != 0
		ORDER BY 1, 2 DESC, 3;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM tempos_by_genre;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


# def sum_albums_released_by_artist_per_year(conn):
#     SELECT
#         year, 
#         SUM(total_albums),
#         artist
#     FROM (
#             SELECT
#                 strftime('%Y', alb.release_date) year,
#                 COUNT(alb.album_name) total_albums,
#                 a.artist_name artist
#             FROM album alb
#             JOIN artist a
#                 ON a.artist_id = alb.artist_id 
#             WHERE artist = 'Becky G'
#             GROUP BY 3, strftime('%Y', alb.release_date)
#             ORDER BY 3, 1) AS alb_by_year
#     GROUP BY year           
		
# 		SELECT
#             strftime('%Y', alb.release_date) release_date,
#             COUNT(alb.album_name) total_albums,
#             a.artist_name artist_name
#         FROM album alb
#         JOIN artist a
#             ON a.artist_id = alb.artist_id 
# 		GROUP BY 3, strftime('%Y', alb.release_date)
#         ORDER BY 3, 1


def valence_popularity_by_genre(conn):
    """
    Query valence vs popularity by genre
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS valence_popularity_by_genre;")
    create_view = """
        CREATE VIEW IF NOT EXISTS valence_popularity_by_genre
        AS
        SELECT
            a.genre,
            printf('%.3f', AVG(f.valence)) valence,
			printf('%.1f', AVG(a.popularity)) popularity
        FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id 
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f 
            ON f.track_id = t.track_id
        GROUP BY 1
        ORDER BY 1;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM valence_popularity_by_genre;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def valence_popularity_by_artist(conn):
    """
    Query valence vs popularity by artist
    :param conn: the Connection object
    :return: view
    """   
    cur = conn.cursor()
    cur.execute("DROP VIEW IF EXISTS valence_popularity_by_artist;")
    create_view = """
        CREATE VIEW IF NOT EXISTS valence_popularity_by_artist
        AS
        SELECT
            a.artist_name artist,
            printf('%.3f', AVG(f.valence)) valence,
			printf('%.1f', AVG(a.popularity)) popularity
        FROM artist a
        JOIN album alb
            ON a.artist_id = alb.artist_id 
        JOIN track t
            ON t.album_id = alb.album_id
        JOIN track_feature f 
            ON f.track_id = t.track_id
        GROUP BY 1
        ORDER BY 1;
    """

    cur.execute(create_view)
    conn.commit()

    select_query = """
        SELECT *
        FROM valence_popularity_by_artist;
    """
    cur.execute(select_query)

    view = from_db_cursor(cur)
    print(view)


def main():
    database = "spotify.db"

    # Create a database connection
    conn = create_connection(database)
    with conn:
        # 1: top 10 songs per artist in terms of duration_ms
        top_10_songs_by_duration_per_artist(conn)

        # 2: top 20 artists by the number of followers
        top_20_artists_by_followers(conn)

        # 3: top 10 songs per artist in terms of tempo
        top_10_songs_by_tempo_per_artist(conn)

        # 4: artists with the most albums and songs
        num_songs_albums_by_artist(conn)

        # 5: albums released in the 90s
        albums_released_in_90s(conn)

        # 6: top 20 songs with the highest danceability
        top_20_songs_by_danceability(conn)

        # 7: avg energy of artist
        avg_energy_of_artist(conn)

        # 8: artists who have more than 20 albums
        artists_w_atleast_20_albums(conn)

        # 9: avg audio features of all the songs in each genre
        avg_audio_features_by_genre(conn)

        # 10: loudness vs energy by genre
        loudness_energy_by_genre(conn)

        # 11: avg audio features by artist
        avg_audio_features_by_artist(conn)

        # 12: correlation of audio features
        audio_features_correlations(conn)

        # 13: the audio features for Jack Harlow's album, Come Home The Kids Miss You
        audio_features_for_album(conn)

        # 14: popularity and genre of artists
        popularity_by_artists_in_genre(conn)

        # 15: tempos of songs by genre
        tempos_by_genre(conn)

        # 16: valence vs popularity by genre
        valence_popularity_by_genre(conn)    

        # 17: valence vs popularity by artist  
        valence_popularity_by_artist(conn) 

if __name__ == '__main__':
    main()
    
