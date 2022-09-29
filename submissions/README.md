<h1 align="center">Onramp Data Engineering Take Home Project</h1>

<h2 align="center"> Yesenia Ramirez </h2>

<p align="center">This project includes data from 20 of my favorite artists. I have pulled this data from Spotify and it includes details about the artist, their albums, tracks and track audio features. There are views and visualizations created to see correlations between all the data.</p>
<hr>

## Technologies Used 
<img src="https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"> <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white"> <img src="https://img.shields.io/badge/Matplotlib-07405E?style=for-the-badge&logo="> <img src="https://img.shields.io/badge/seaborn-07405E?style=for-the-badge&logo=">
<br>
<br>

## Installation/Setup
1. Git fork and clone this repo and navigate into ```/onramp_project/submissions``` directory
```sh
cd onramp_project/submissions
```
2. Create a virtual environment 
```sh
python -m venv .venv
```
3. Activate the environment
```sh
source .venv/bin/activate
```
4. Update pip
```sh
python -m pip install --upgrade pip
```
5. Install requirements
```sh
pip install -r requirements.txt
```
6. Get your <a href="https://developer.spotify.com/dashboard/login">Spotify Authentication Credentials</a>. You can follow this <a href="https://youtu.be/3RGm4jALukM">YouTube tutorial</a> provided by <a href="https://spotipy.readthedocs.io/en/master/">Spotipy</a>.
7. Create an ```.env``` file and set your environment variables
```sh
SPOTIPY_CLIENT_ID=""
SPOTIPY_CLIENT_SECRET=""
SPOTIPY_REDIRECT_URI=""
```
8. Open your choice of database manager/editor, I used *DB Browser for SQLite*, and open the ```spotify.db``` file to view all the data of my favorite 20 artists
<br>
<br>

## Data Tables
#### Artist

|    column    |   datatype   |                              example                             |
|:------------:|:------------:|:----------------------------------------------------------------:|
|   artist_id  |  varchar(50) |                      7jy3rLJdDQY21OgRLCZ9sD                      |
|  artist_name | varchar(255) |                           Foo Fighters                           |
| external_url | varchar(100) |      https://open.spotify.com/artist/7jy3rLJdDQY21OgRLCZ9sD      |
|     genre    | varchar(100) |                         alternative metal                        |
|   image_url  | varchar(100) | https://i.scdn.co/image/ab6761610000e5eb9a43b87b50cd3d03544bb3e5 |
|   followers  |      int     |                             10156976                             |
|  popularity  |      int     |                                77                                |
|     type     |  varchar(50) |                              artist                              |
|  artist_uri  | varchar(100) |               spotify:artist:7jy3rLJdDQY21OgRLCZ9sD              |
<br>

#### Album

|    column    |   datatype   |                              example                             |
|:------------:|:------------:|:----------------------------------------------------------------:|
|   album_id   |  varchar(50) |                      2FfewmvnA0wctMD64KjOxP                      |
|  album_name  | varchar(255) |                            Dream Widow                           |
| external_url | varchar(100) |       https://open.spotify.com/album/2FfewmvnA0wctMD64KjOxP      |
|   image_url  | varchar(100) | https://i.scdn.co/image/ab67616d0000b273a57abaeb967f055948170bd6 |
| release_date |     date     |                            2022-03-25                            |
| total_tracks |      int     |                                 8                                |
|     type     |  varchar(50) |                               album                              |
|   album_uri  | varchar(100) |               spotify:album:2FfewmvnA0wctMD64KjOxP               |
|   artist_id  |  varchar(50) |                      7jy3rLJdDQY21OgRLCZ9sD                      |
<br>

#### Track
|    column    |   datatype   |                        example                        |
|:------------:|:------------:|:-----------------------------------------------------:|
|   track_id   |  varchar(50) |                 5k8kaD41vSP6l0Jhe9HzmY                |
| song_name    | varchar(255) |                         Encino                        |
| external_url | varchar(100) | https://open.spotify.com/track/5k8kaD41vSP6l0Jhe9HzmY |
|  duration_ms |      int     |                         98293                         |
|   explicit   |    boolean   |                          TRUE                         |
|  disc_number |      int     |                           1                           |
|     type     |  varchar(50) |                         track                         |
|   song_uri   | varchar(100) |          spotify:track:5k8kaD41vSP6l0Jhe9HzmY         |
|   album_id   |  varchar(50) |                 2FfewmvnA0wctMD64KjOxP                |
<br>

#### Track_Feature
|      column      |   datatype   |                example               |
|:----------------:|:------------:|:------------------------------------:|
|     track_id     |  varchar(50) |        5k8kaD41vSP6l0Jhe9HzmY        |
|   danceability   |    double    |                 0.277                |
|      energy      |    double    |                 0.992                |
| instrumentalness |    double    |                 0.836                |
|     liveness     |    double    |                 0.272                |
|     loudness     |    double    |                -6.237                |
|    speechiness   |    double    |                0.0856                |
|       tempo      |    double    |                103.494               |
|       type       |  varchar(50) |            audio_features            |
|      valence     |    double    |                 0.148                |
|     song_uri     | varchar(100) | spotify:track:5k8kaD41vSP6l0Jhe9HzmY |
<br>

## Directory Tree
* [submissions/](.)
    * [data_code/](./data_code)
        * [d1_tables.py](./data_code/d1_tables.py)
        * [d2_db.py](./data_code/d2_db.py)
        * [d3_views.py](./data_code/d3_views.py)
        * [d4_visualizations.py](./data_code/d4_visualizations.py)
    * [jupyter_notebooks/](./jupyter_notebooks)
        * [views.ipynb](./jupyter_notebooks/views.ipynb)
        * [visualizations.ipynb](./jupyter_notebooks/visualizations.ipynb)
    * [visualization_imgs/](./visualization_imgs)
        * [audio_feature_correlations.png](./visualization_imgs/audio_feature_correlations.png)
        * [avg_audio_features_by_artist.png](./visualization_imgs/avg_audio_features_by_artist.png)
        * [tempos_by_genre_strip.png](./visualization_imgs/tempos_by_genre_strip.png)
        * [tempos_by_genre_violin.png](./visualization_imgs/tempos_by_genre_violin.png)
        * [top_20_artists_by_followers.png](./visualization_imgs/top_20_artists_by_followers.png)
        * [valence_popularity_by_artist.png](./visualization_imgs/valence_popularity_by_artist.png)
        * [valence_popularity_by_genre.png](./visualization_imgs/valence_popularity_by_genre.png)
    * [.gitignore](./.gitignore)
    * [README.md](./README.md)
    * [requirements.txt](./requirements.txt)
    * [spotify.db](./spotify.db)
    * [visualizations.pdf](./visualizations.pdf)
<br>
<br>

## File Code Explanation

[<h3>```submissions/```</h3>](.) 

[```d1_tables.py```](./data_code/d1_tables.py)
- This python file is where I created all my tables necessary for my database
    - artist
    - album
    - track
    - track_feature
- It also holds my create_connection function, which creates a connection to the SQLite database 

You can run this file to create the tables or create the tables at the same time as insertion. 
```sh
python data_code/d1_tables.py
```
<br>

[```d2_db.py```](./data_code/d2_db.py)
- This python file contains my ETL code using ```Spotipy```, ```Pandas```, ```SQL```, and ```Python```. 
- ```check_if_valid_data``` checks the data frame for any null values and if the data frame is empty
- There are 4 functions that are specific to one table in the database
    - ```insert_artists``` creates the artist table, searches for all my favorite artists in the ```fav_artists``` list, pulls the data, and inserts it into the database. 
    - ```insert_albums``` creates the album table, searches for the artist's albums with the artist_id, pulls the data, and inserts it into the database. 
        - I filtered out duplicate albums by identifying if they had the same album_name and were both by the same artist. 
        - I filtered out Deluxe Editions by looking for a couple of different variations of 'Deluxe Edition', without the possibility of filtering out albums with the word 'Deluxe' in the name. 
            - This removed majority of the Deluxe albums, but there were some outliers that weren't removed. 
    - ```insert_tracks``` creates the track table, searches for the album's tracks with the album_id, pulls the data, and inserts it into the database. 
    - ```insert_feature``` creates the track_feature table, searches for the track's audio features with a list of a maximum of 100 track_ids to reduce the number of API calls, pulls the data, and inserts it into the database. 

You can run this file to create the tables, pull, transform, and insert the data into the database. 
```sh
python data_code/d2_db.py
```
<br>

[```d3_views.py```](./data_code/d3_views.py)
- This python file is where I created all my SQLite views so the data can be analyzed. 
- There are a variety of 17 different views 
    - Top 10 songs per artist in terms of duration_ms
    - Top 20 artists by the number of followers
    - Top 10 songs per artist in terms of tempo
    - Artists listed by the number of albums and songs
    - Albums released in the 90s
    - Top 20 songs with the highest danceability
    - Average energy of all the artists
    - Artists who have more than 20 albums
    - Average audio features of all the songs in each genre
    - Loudness vs energy by genre
    - Average audio features by artist
    - Correlation of certain audio features
    - The audio features for Jack Harlow's album, Come Home The Kids Miss You
    - Popularity and genre of artists
    - Tempos of songs by genre 
    - Valence vs popularity by genre    
    - Valence vs popularity by artist 

You can run this file to create the views and insert them into the database. They also print in the terminal via ```prettytable```. 
```sh
python data_code/d3_views.py
```
*Jupyter version available at [```jupyter_notebooks/views.ipynb```](./jupyter_notebooks/views.ipynb)*

<br>

[```d4_visualizations.py```](./data_code/d4_visualizations.py)
- This python file contains the code to create 7 data visualizations using ```matplotlib``` and ```seaborn```. 
- There are 7 different visualizations 
    - Bar plot: top 20 artists by followers 
    - Violin plot: tempos based on genre
    - Strip plot: tempos based on genre 
    - LM plot: valence vs popularity based on artist
    - LM plot: valence vs popularity based on genre 
    - Heat map: track audio feature correlations
    - Pair plot: track audio features relationship

*[visualizations.pdf](./visualizations.pdf) goes into more detail about the graphs*

You can run this file to create the visualizations
```sh
python data_code/visualizations.py
```
*Jupyter version available at [```jupyter_notebooks/visualizations.ipynb```](./jupyter_notebooks/visualizations.ipynb)*

<br>
<br>

## Author

👤 **Yesenia Ramirez**

* Portfolio Website: [yeseniar.dev](https://www.yeseniar.dev)
* Github: [@yeseniaramirez14](https://github.com/yeseniaramirez14)
* LinkedIn: [@yeseniaramirez14](https://linkedin.com/in/yeseniaramirez14)
