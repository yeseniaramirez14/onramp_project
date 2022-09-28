import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from tables import create_connection


rcParams.update({'figure.autolayout': True})


def top_20_artists_by_followers_vis(conn):
    df = pd.read_sql_query("SELECT * FROM top_20_artists_by_followers", conn)
    plt.figure(figsize=(14,5))
    ax = sns.barplot(df, y='artist_name', x="followers", hue="genre", dodge=False)
    ax.set_title("Top 20 Artists by Followers", fontsize='large', fontweight='bold')
    ax.set_ylabel("Artist Name")
    ax.set_xlabel("Number of Followers (in tens of millions)")
    plt.legend(title="Genre")
    plt.savefig("visualization_imgs/top_20_artists_by_followers")
    plt.show()


def tempos_by_genre_violin_vis(conn):
    df = pd.read_sql_query("SELECT * FROM tempos_by_genre;", conn)
    plt.figure(figsize=(12,5))
    g = sns.violinplot(x='genre', y='tempo', data=df)
    g.set(xlabel='Genre', ylabel='Tempo (beats per minute)', title='Tempos by Genre')
    plt.xticks(rotation = 30, rotation_mode='anchor', ha='right')
    plt.savefig("visualization_imgs/tempos_by_genre_violin")
    plt.show()


def tempos_by_genre_strip_vis(conn):
    df = pd.read_sql_query("SELECT * FROM tempos_by_genre;", conn)
    plt.figure(figsize=(12,6))
    g = sns.stripplot(x='genre', y='tempo', hue='artist_name', data=df)
    g.set(xlabel='Genre', ylabel='Tempo (beats per minute)', title='Tempos by Genre')
    plt.xticks(rotation = 30, rotation_mode='anchor', ha='right')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, title="Artists")
    plt.savefig("visualization_imgs/tempos_by_genre_strip")
    plt.show()


def valence_popularity_by_genre_vis(conn):
    df = pd.read_sql_query("SELECT * FROM valence_popularity_by_genre", conn)

    type_dic = {
        "popularity": "float64",
        "valence": "float64"
    }
    df = df.astype(type_dic)
    markers = ["<", ">", "^", "v", "p", "X", "s", "D", "o", "d", "P","*","H"]
    g = sns.lmplot(x='valence', y='popularity', data=df, hue="genre", legend=False, aspect=2, markers=markers)
    g.set(xlabel='Valence', ylabel='Popularity', title='Valence vs Popularity by Genre', xlim=(0,1), ylim=(0,100))
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, title="Genre")
    plt.savefig("visualization_imgs/valence_popularity_by_genre")
    plt.show()


def valence_popularity_by_artist_vis(conn):
    df = pd.read_sql_query("SELECT * FROM valence_popularity_by_artist", conn)

    type_dic = {
        "popularity": "float64",
        "valence": "float64"
    }
    df = df.astype(type_dic)
    markers = ["<", ">", "^", "v", "p", "X", "s", "D", "o", "d", "P","*","H", "<", ">", "^", "v", "p", "X", "s"]
    g = sns.lmplot(x='valence', y='popularity', data=df, hue="artist", legend=False, aspect=2, markers=markers)
    g.set(xlabel='Valence', ylabel='Popularity', title='Valence vs Popularity by Artist', xlim=(0,1), ylim=(0,105))
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, title="Genre")
    plt.savefig("visualization_imgs/valence_popularity_by_artist")
    plt.show()


def audio_features_correlations_vis(conn):
    ds = pd.read_sql_query("SELECT * FROM audio_features_correlations", conn)
    ds = ds.astype("float64")
    plt.figure(figsize=(8,6))
    pc = ds.corr(method ='pearson')
    ax = sns.heatmap(pc, annot=True, annot_kws={'size': 10})
    ax.set(title="Audio Feature Correlations")
    plt.xticks(rotation = 30, rotation_mode='anchor', ha='right')
    plt.savefig("visualization_imgs/audio_feature_correlations")
    plt.show()


def avg_audio_features_by_artist_vis(conn):
    ds = pd.read_sql_query("SELECT * FROM avg_audio_features_by_artist", conn)
    type_dic = {
        "Energy": "float64",
        "Danceability": "float64",
        "Tempo": "float64",
        "Instrumentalness": "float64",
        "Valence": "float64"
    }
    ds = ds.astype(type_dic)
    markers = ["<", ">", "^", "v", "p", "X", "s", "D", "o", "d", "P","*","H", "<", ">", "^", "v", "p", "X", "s"]
    sns.pairplot(ds, x_vars=["Energy", "Danceability", "Tempo", "Instrumentalness", "Valence"], y_vars=["Energy", "Danceability", "Tempo", "Instrumentalness", "Valence"], hue="Artist", corner=True, markers=markers, height=2)
    plt.suptitle("Average Audio Features by Artist", fontsize='large', fontweight='bold')
    plt.savefig("visualization_imgs/avg_audio_features_by_artist") 
    plt.show()


def main():
    database = "spotify.db"

    # create a database connection
    conn = create_connection(database)
    with conn:

        top_20_artists_by_followers_vis(conn)

        tempos_by_genre_violin_vis(conn)

        tempos_by_genre_strip_vis(conn)

        valence_popularity_by_genre_vis(conn)

        valence_popularity_by_artist_vis(conn)

        audio_features_correlations_vis(conn)

        avg_audio_features_by_artist_vis(conn)


if __name__ == '__main__':
    main()