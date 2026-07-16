import pandas as pd
import ast
# ==================================================
# Funciones auxiliares
# ==================================================

def fix_unicode(text):
    """
    Elimina caracteres Unicode inválidos (surrogates) de una cadena de texto.
    """
    if not isinstance(text, str):
        return text

    return "".join(
        c for c in text
        if not (0xD800 <= ord(c) <= 0xDFFF)
    )
def normalize_text(series):
    """Pasa texto a minúsculas y elimina espacios extra."""
    return (
        series
        .apply(fix_unicode)
        .str.lower()
        .str.strip()
    )

def remove_special_characters(series):
    """Elimina signos de puntuación comunes (! ? .) y caracteres no alfanuméricos."""
    return series.str.replace(
    r"[^\w\s'-]",
    "",
    regex=True
    )


def parse_string_list(series):
    """Convierte strings tipo '["a", "b"]' en listas reales. Devuelve lista vacía si falla."""
    
    def safe_parse(x):
            try:
                result = ast.literal_eval(x)
                return result if isinstance(result, list) else [result]
            except (ValueError, SyntaxError):
                return []

    return series.apply(safe_parse)

def clean_list_of_strings(series):
    """
    Convierte el texto de las listas a minúsculas, elimina espacios y
    elimina elementos duplicados manteniendo el orden.
    """
    return series.apply(
        lambda x: list(
            dict.fromkeys(
                fix_unicode(item).lower().strip()
                for item in x
            )
        ) if isinstance(x, list) else []
    )

def clean_songs(df):
    """
    Limpieza y transformación del dataset songs.

    Parámetros:
    df: DataFrame original
    """
    df = df.copy()

    # ------------------
    # IDs
    # ------------------
    df["id"] = normalize_text(df["id"])

    # ------------------
    # Name & Album
    # ------------------
    df["name"] = normalize_text(df["name"])
    df["name"] = remove_special_characters(df["name"])
    df["name"] = df["name"].replace("nan", pd.NA)

    df["album_name"] = normalize_text(df["album_name"])
    df["album_name"] = remove_special_characters(df["album_name"])
    df["album_name"] = df["album_name"].replace("nan", pd.NA)

    # ------------------
    # Genre
    # ------------------
    df["genre"] = df["genre"].astype(str).str.lower().str.strip()

    # ------------------
    # Artists
    # ------------------
    df["artists"] = parse_string_list(df["artists"])
    df["artists"] = clean_list_of_strings(df["artists"])
    df["n_artists"] = df["artists"].apply(len)
    df["main_artist"] = df["artists"].apply(lambda x: x[0] if x else pd.NA)

    # ------------------
    # Artist IDs
    # ------------------
    df["artist_ids"] = parse_string_list(df["artist_ids"])
    df["artist_ids"] = clean_list_of_strings(df["artist_ids"])

    # ------------------
    # Niche genres
    # ------------------
    df["niche_genres"] = parse_string_list(df["niche_genres"])
    df["niche_genres"] = clean_list_of_strings(df["niche_genres"])
    df["n_niche_genres"] = df["niche_genres"].apply(len)

    # ------------------
    # Mode
    # ------------------
    df["mode"] = df["mode"].fillna(-1).map({0: "minor", 1: "major"}).replace({-1: pd.NA})

    # ------------------
    # Decade
    # ------------------
    df["decade"] = (
    ((df["year"] // 10) * 10)
    .astype("Int64")
    )

    df["decade"] = df["decade"].apply(
    lambda x: f"{x}s" if pd.notna(x) else pd.NA
    )
def clean_artists(df):
    """
    Limpieza y transformación del dataset artists.

    Parámetros:
    df: DataFrame original
    """

    df = df.copy()

    # ------------------
    # ID
    # ------------------
    df["id"] = normalize_text(df["id"])

    # ------------------
    # Name
    # ------------------
    df["name"] = normalize_text(df["name"])
    df["name"] = remove_special_characters(df["name"])
    df["name"] = df["name"].replace("nan", pd.NA)

    # ------------------
    # Genres
    # ------------------
    df["genres"] = parse_string_list(df["genres"])
    df["genres"] = clean_list_of_strings(df["genres"])

    # ------------------
    # Main genre
    # ------------------
    df["main_genre"] = normalize_text(df["main_genre"])

    # ------------------
    # Variables auxiliares
    # ------------------
    df["n_genres"] = df["genres"].apply(len)

    # ------------------
    # Popularity
    # ------------------
    df["popularity"] = df["popularity"].clip(0, 100)

    # ------------------
    # Limpiar caracteres Unicode inválidos
    # ------------------
    text_columns = df.select_dtypes(include=["object", "string"]).columns

    for col in text_columns:
        df[col] = df[col].apply(fix_unicode)

    return df
    # ------------------
    # Popularity per million followers
    # ------------------
    
    followers = df["total_artist_followers"].replace(0, pd.NA)
    followers = followers.where(followers > 0)

    df["popularity_per_million_followers"] = (
    df["popularity"] /
    (followers/1_000_000)
    ).round(2)

    # ------------------
    # Transformaciones extra
    # ------------------
    if "duration_ms" in df.columns:
        df["duration_min"] = (df["duration_ms"] / 60000).round(2)

    # ------------------
    # Drop lyrics
    # ------------------
    df = df.drop(columns=["lyrics"], errors="ignore")

    return df
