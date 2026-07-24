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
        except (ValueError, SyntaxError, TypeError):
            return []

    return series.apply(safe_parse)


def merge_songs_artists(songs_df, artists_df):
    """
    Prepara el dataset final de música manteniendo
    una única fila por canción.

    El dataset songs ya contiene las variables de artista
    agregadas previamente, por lo que no es necesario
    volver a hacer un merge con artists.
    """

    # ------------------
    # Copias de seguridad
    # ------------------

    music = songs_df.copy()

    # ------------------
    # Convertir artist_ids
    # en listas reales
    # ------------------

    music["artist_ids"] = parse_list_column(
        music["artist_ids"]
    )

    # ------------------
    # Colaboraciones
    # 0 = No colaboración
    # 1 = Colaboración
    # ------------------

    music["is_collaboration"] = (
        music["n_artists"] > 1
    ).astype(int)

    # ------------------
    # Tiene géneros de nicho
    # ------------------

    music["artist_has_genres"] = (
        music["n_niche_genres"] > 0
    )

    # ------------------
    # Seguidores en millones
    # ------------------

    music["artist_followers_millions"] = (
        music["total_artist_followers"] / 1_000_000
    ).round(2)

    # ------------------
    # Comprobar duplicados
    # ------------------

    music = music.drop_duplicates(
        subset="id"
    ).reset_index(drop=True)

    # ------------------
    # Renombrar columnas
    # ------------------

    music = music.rename(
        columns={
            "id": "song_id",
            "name": "song_name",
            "popularity": "song_popularity"
        }
    )

    return music