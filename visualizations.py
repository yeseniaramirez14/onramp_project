import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from tables import create_connection

rcParams.update({'figure.autolayout': True})


# this one works!
def top_artists_by_followers_vis(conn):
    df = pd.read_sql_query("SELECT * FROM top_20_artists_by_followers", conn)
    plt.figure(figsize=(14,5))
    plt.tight_layout()
    ax = sns.barplot(df, y='artist_name', x="followers", hue="genre", dodge=False)
    ax.set_title("Top Artists by Followers")
    ax.set_ylabel("Artist Name")
    ax.set_xlabel("Number of Followers")
    plt.legend(title="Genre")
    plt.show()


# needs work
def top_songs_by_duration_vis(conn):
    df = pd.read_sql_query("SELECT * FROM top_10_songs_by_duration_per_artist", conn)
    plt.figure(figsize=(14,5))
    plt.tight_layout()
    ax = sns.barplot(df, y="song_name", x="duration_ms", dodge=False)
    ax.set_title("Top Song of Artists by Duration")
    ax.set_ylabel("Song Name")
    ax.set_xlabel("Song Duration (ms)")
    plt.legend(title="Genre")
    plt.show()


def energy_danceability_by_genre(conn):
    df = pd.read_sql_query("SELECT * FROM avg_audio_features_by_genre", conn)
    g = sns.lmplot(x='energy', y='loudness', data=df, hue="genre", legend=False, aspect=2,)
    g.set(xlabel='Energy', ylabel='Loudness', title='Energy vs Loudness by Genre')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, title="Genre")
    plt.show()


def loudness_energy_by_genre_vis(conn):
    df = pd.read_sql_query("SELECT * FROM loudness_energy_by_genre", conn)
    g = sns.lmplot(x='energy', y='loudness', data=df, hue="genre", legend=False, aspect=2,)
    g.set(xlabel='Energy', ylabel='Loudness', title='Energy vs Loudness by Genre')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, title="Genre")
    plt.show()


def audio_features_for_album_vis(conn):
    df = pd.read_sql_query("SELECT * FROM avg_audio_features_by_genre", conn)
    sns.relplot(data=df, x="popularity", y='energy', col='genre', hue='genre', row='energy', kind='line')
    g = sns.FacetGrid(df, col='genre', hue='genre')
    g.map(plt.plot, 'popularity')
    plt.show()


def avg_audio_features_by_artist(conn):
    df = pd.read_sql_query("SELECT * FROM avg_audio_features_by_artist", conn)
    g = sns.boxplot(df)
    g.set(ylim=(0,1), title='Average Audio Features by Artist')
    plt.show()


def popularity_by_artists_in_genre_vis(conn):
    df = pd.read_sql_query("SELECT * FROM popularity_by_artists_in_genre;", conn)
    sns.violinplot(y='genre', x='popularity', data=df)
    # plt.xticks(rotation = 90)
    plt.show()

def tempos_by_genre_violin_vis(conn):
    df = pd.read_sql_query("SELECT * FROM tempos_by_genre;", conn)
    plt.figure(figsize=(12,5))
    plt.tight_layout()
    g = sns.violinplot(x='genre', y='tempo', data=df)
    g.set(xlabel='Genre', ylabel='Tempo', title='Tempos by Genre')
    plt.xticks(rotation = 30, rotation_mode='anchor', ha='right')
    plt.show()

def tempos_by_genre_strip_vis(conn):
    df = pd.read_sql_query("SELECT * FROM tempos_by_genre;", conn)
    plt.figure(figsize=(12,6))
    g = sns.stripplot(x='genre', y='tempo', hue='artist_name', data=df)
    g.set(xlabel='Genre', ylabel='Tempo', title='Tempos by Genre')
    plt.xticks(rotation = 30, rotation_mode='anchor', ha='right')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, title="Artists")
    plt.show()


# not using this -- too overwhelmed 
def tempos_by_genre_overlay_vis(conn):
    df = pd.read_sql_query("SELECT * FROM tempos_by_genre;", conn)
    plt.figure(figsize=(12,6))
    sns.violinplot(x='genre', y='tempo', data=df)
    g = sns.stripplot(x='genre', y='tempo', data=df, color='k', alpha=0.4)
    g.set(xlabel='Genre', ylabel='Tempo', title='Tempos by Genre')
    plt.xticks(rotation = 30, rotation_mode='anchor', ha='right')
    plt.show()


def pairplots(conn):
    ds = pd.read_sql_query("SELECT * FROM audio_features_by_genre", conn)
    sns.pairplot(ds[['danceability', 'tempo', 'genre', 'popularity']], hue="genre")
    plt.show()

#********************************************

# def audio_features_by_genre2_vis(conn):
#     followers = pd.read_sql_query("SELECT * FROM audio_features_by_genre", conn)

#     sns.set_theme()
#     # set figure size
#     plt.figure(figsize=(20,10))

#     # plot polar axis
#     ax = plt.subplot(111, polar=True)

#     # remove grid
#     plt.axis('off')

#     # Set the coordinates limits
#     upperLimit = 150
#     lowerLimit = -15

#     # Compute max and min in the dataset
#     max = followers['danceability'].max()

#     # Let's compute heights: they are a conversion of each item value in those new coordinates
#     # In our example, 0 in the dataset will be converted to the lowerLimit (10)
#     # The maximum will be converted to the upperLimit (100)
#     slope = (max - lowerLimit) / max
#     heights = slope * followers.values + lowerLimit

#     # Compute the width of each bar. In total we have 2*Pi = 360°
#     width = 2*np.pi / len(df.index)

#     # Compute the angle each bar is centered on:
#     indexes = list(range(1, len(df.index)+1))
#     angles = [element * width for element in indexes]
#     angles
    
#     # Draw bars
#     bars = ax.bar(
#         x=angles, 
#         height=heights, 
#         width=width, 
#         bottom=lowerLimit,
#         linewidth=2, 
#         edgecolor="white")

#     # little space between the bar and the label
#     labelPadding = 4

#     # Add labels
#     for bar, angle, height, label in zip(bars,angles, heights, followers["genre"]):

#         # Labels are rotated. Rotation must be specified in degrees
#         rotation = np.rad2deg(angle)

#         # Flip some labels upside down
#         alignment = ""
#         if angle >= np.pi/2 and angle < 3*np.pi/2:
#             alignment = "right"
#             rotation = rotation + 180
#         else: 
#             alignment = "left"

#         # Finally add the labels
#         ax.text(
#             x=angle, 
#             y=lowerLimit + bar.get_height() + labelPadding, 
#             s=label, 
#             ha=alignment, 
#             va='center', 
#             rotation=rotation, 
#             rotation_mode="anchor") 




#     # sns.barplot(followers, x="danceability", y="genre")
#     # plt.show()

# def line_graph(conn):
#     df = pd.read_sql_query("SELECT * FROM audio_features_for_album", conn)
#     # print(df.shape)
#     # print(df.columns)
#     # cols = ['energy','danceability', 'tempo']
#     cols = df.columns
#     rows = df.values
#     # print("lengthhhhhh", df.values)
#     # sns.set(rc={'figure.figsize':(14,6)})
#     ax = sns.lineplot(data=df, x="song_name", y='energy', markers=True, errorbar=None)
#     plt.show()


# def line_graph1(conn):
#     df = pd.read_sql_query("SELECT * FROM audio_features_by_genre", conn)
#     print(df.shape)
#     sns.set(rc={'figure.figsize':(14,6)})
#     ax = sns.lineplot(data=df, x="energy", y="popularity", markers=True, errorbar=None)
#     plt.show()

# def bar_plot(conn):
#     df = pd.read_sql_query("SELECT * FROM audio_features_by_genre", conn)
#     print(df.shape)
#     sns.set(rc={'figure.figsize':(14,6)})
#     ax = sns.barplot(data=df, x="energy", y="popularity", hue="genre", errorbar=None)
#     plt.show()

# def scatter_plot(conn):
#     df = pd.read_sql_query("SELECT * FROM audio_features_by_genre", conn)
#     print(df.shape)
#     df.columns
#     print(df.columns)
#     sns.set(rc={'figure.figsize':(14,6)})
#     ax = sns.scatterplot(data=df, x="energy", y="popularity", hue="genre", style="genre")
#     plt.show()

# def subplots(conn):
#     df = pd.read_sql_query("SELECT * FROM audio_features_by_genre", conn)
#     fig, axes = plt.subplots(2, 2, figsize=(12, 7))

#     a = df["energy"].values
#     b = df["danceability"].values 
#     c = df["tempo"].values

#     # plot 1
#     sns.distplot(a, color = 'blue', ax=axes[0,0])

#     # plot 2
#     sns.distplot(b, color = 'blue', ax=axes[0,1])

#     # plot 3
#     sns.distplot(c, color = 'blue', ax=axes[1,0])

#     # ax = sns.scatterplot(data=ds, x="energy", y="popularity", hue="genre", style="genre")
#     plt.show()



# def heatmap(conn):
#     ds = pd.read_sql_query("SELECT * FROM audio_features_by_genre", conn)
#     pc = ds[['energy','danceability', 'genre', 'popularity']].corr(method ='pearson')

#     cols = ['energy','danceability', 'tempo']
#     y = ['popularity']

#     ax = sns.heatmap(pc, annot=True,
#                     yticklabels=y,
#                     xticklabels=cols,
#                     annot_kws={'size': 50})

#     plt.show()






# # https://seaborn.pydata.org/tutorial/function_overview.html
# # sns.displot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")

def main():
    database = "spotify.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("BARPLOT: Visualization of top artists by followers")
        # top_artists_by_followers_vis(conn)

        # print("BARPLOT: Visualization of top songs by duration")
        # top_songs_by_duration_vis(conn)

        # print("LMPLOT: Visualization of energy vs danceability by genre")
        # energy_danceability_by_genre(conn)

        print("LMPLOT: Visualization of energy vs danceability by genre")
        loudness_energy_by_genre_vis(conn)

        # print("RELPLOT: Visualization of audio features for album")
        # audio_features_for_album_vis(conn)

        # print("BOXPLOT: Visualization of the average audio features by artist")
        # avg_audio_features_by_artist(conn)

        # print("VIOLINPLOT: Visualization of artist's popularity in genre")
        # popularity_by_artists_in_genre_vis(conn)

        # print("VIOLINPLOT: Visualization of average tempos by genre")
        # tempos_by_genre_violin_vis(conn)
        
        # print("STRIPPLOT: Visualization of song tempos by genre and artist")
        # tempos_by_genre_strip_vis(conn)

        # print("Visualization of tempos by genre overlayed with tempos by artist")
        # tempos_by_genre_overlay_vis(conn)

        # print("Visualization of danceability, tempo and popularity based on genre")
        # pairplots(conn)

if __name__ == '__main__':
    main()
    
