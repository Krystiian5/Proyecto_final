import pandas as pd
import ast


def parse_list_column(series):
    """
    Convierte una columna almacenada como texto de listas
    en listas reales de Python.
    """

    def safe_parse(x):
        try:
            result = ast.literal_eval(x)
            return result if isinstance(result, list) else []
        except (ValueError, SyntaxError):
            return []

    return series.apply(safe_parse)


def merge_songs_artists(songs_df, artists_df):
    """
    Une los datasets limpios de canciones y artistas.
    """

    songs = songs_df.copy()
    artists = artists_df.copy()

    # ------------------
    # Convertir listas
    # ------------------

    songs["artist_ids"] = parse_list_column(songs["artist_ids"])

    # ------------------
    # Una fila por artista
    # ------------------

    songs = songs.explode(
        "artist_ids",
        ignore_index=True
    )

    # ------------------
    # Merge
    # ------------------

    music = songs.merge(
        artists,
        left_on="artist_ids",
        right_on="id",
        how="left",
        suffixes=("_song", "_artist")
    )

    # ------------------
    # Renombrar columnas
    # ------------------

    music = music.rename(
        columns={
            "id_song": "song_id",
            "name_song": "song_name",
            "popularity_song": "song_popularity",

            "id_artist": "artist_id",
            "name_artist": "artist_name",
            "popularity_artist": "artist_popularity",

            "followers": "artist_followers",
            "genres": "artist_genres",

            "duration_min": "song_duration_min"
        }
    )

    # ------------------
    # Variables auxiliares
    # ------------------

    music["is_collaboration"] = music["n_artists"] > 1

    music["artist_has_genres"] = (
        music["n_genres"] > 0
    )

    music["artist_followers_millions"] = (
        music["artist_followers"] / 1_000_000
    ).round(2)

    # ------------------
    # Eliminar columnas duplicadas
    # ------------------

    music = music.drop(
        columns=["artist_ids"],
        errors="ignore"
    )

    return music