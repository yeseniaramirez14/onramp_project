<h1 align="center">Onramp Data Engineering Take Home Project</h1>

<h2 align="center"> Yesenia Ramirez </h2>

<p align="center">This project includes data from 20 of my favorite artists. I have pulled this data from Spotify and it includes details about the artist, their albums, tracks and track audio features. There are views and visualizations created to see correlations between all the data.</p>
<hr>

## Technologies Used 
<img src="https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"> <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white"> <img src="https://img.shields.io/badge/Matplotlib-07405E?style=for-the-badge&logo="> <img src="https://img.shields.io/badge/seaborn-07405E?style=for-the-badge&logo=">
<br>
<br>

## Installation/Setup
1. Git fork and clone this repo and navigate into ```/onramp_project``` directory
```sh
cd onramp_project
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

## File Structure
```tables.py```
- This python file is where I created all my tables necessary for my database
    - artist
    - album
    - track
    - track_feature
- It also holds my create_connection function, which creates a connection to the SQLite database 

You can run this file to create the tables or create the tables at the same time as insertion. 
```sh
python tables.py
```
<br>

```db.py```
- This python file contains my ETL code using ```Spotipy```, ```Pandas```, ```SQL```, and ```Python```. 
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
python db.py
```
<br>

```views.py```
- This python file is where I created all my SQLite views so the data can be analyzed. 
- There are a variety of 17 different views 
    1. Top 10 songs per artist in terms of duration_ms
    2. Top 20 artists by the number of followers
    3. Top 10 songs per artist in terms of tempo
    4. Artists listed by the number of albums and songs
    5. Albums released in the 90s
    6. Top 20 songs with the highest danceability
    7. Average energy of all the artists
    8. Artists who have more than 20 albums
    9. Average audio features of all the songs in each genre
    10. Loudness vs energy by genre
    11. Average audio features by artist
    12. Correlation of certain audio features
    13. The audio features for Jack Harlow's album, Come Home The Kids Miss You
    14. Popularity and genre of artists
    15. Tempos of songs by genre 
    16. Valence vs popularity by genre    
    17. Valence vs popularity by artist  

You can run this file to create the views and insert them into the database. They also print in the terminal via ```prettytable```. 
```sh
python views.py
```
<br>

```visualizations.py```
- This python file contains the code to create 7 data visualizations using ```matplotlib``` and ```seaborn```. 
- There are 7 different visualizations 
    1. Bar plot: top 20 artists by followers 
    2. Violin plot: tempos based on genre
    3. Strip plot: tempos based on genre 
    4. LM plot: valence vs popularity based on artist
    5. LM plot: valence vs popularity based on genre 
    6. Heat map: track audio feature correlations
    7. Pair plot: track audio features relationship

You can run this file to create the visualizations
```sh
python visualizations.py
```
<br>


## Author

👤 **Yesenia Ramirez**

* Portfolio Website: [yeseniar.dev](https://www.yeseniar.dev)
* Github: [@yeseniaramirez14](https://github.com/yeseniaramirez14)
* LinkedIn: [@yeseniaramirez14](https://linkedin.com/in/yeseniaramirez14)
