import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from tables import create_connection


def top_artists_by_followers_vis(conn):
    followers = pd.read_sql_query("SELECT * FROM top_artists_by_followers", conn)
    sns.set_theme()
    sns.barplot(followers, y='artist_name', x="num_followers", palette="Set2")
    plt.show()

# https://seaborn.pydata.org/tutorial/function_overview.html
# sns.displot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")

def main():
    database = "spotify.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Visualization of top artists by followers")
        top_artists_by_followers_vis(conn)


if __name__ == '__main__':
    main()
    
