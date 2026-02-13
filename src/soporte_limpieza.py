import pandas as pd
import re
import ast

def normalize_text(series):
    """Pasa texto a minúsculas y elimina espacios extra."""
    return series.astype(str).str.lower().str.strip()

def remove_special_characters(series):
    """Elimina signos de puntuación comunes (! ? .) y caracteres no alfanuméricos."""
    return series.str.replace(r"[^\w\s]", "", regex=True)

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
    """Normaliza texto dentro de listas."""
    return series.apply(lambda x: [item.lower().strip() for item in x] if isinstance(x, list) else [])

def clean_songs(df, drop_columns=None):
    """
    Limpieza y transformación del dataset songs.

    Parámetros:
    df: DataFrame original
    drop_columns: lista de columnas a eliminar del análisis
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
    df["n_niche_genres"] = df["niche_genres"].apply(lambda x: len(x))

    # ------------------
    # Mode
    # ------------------
    df["mode"] = df["mode"].fillna(-1).map({0: "minor", 1: "major"}).replace({-1: pd.NA})

    # ------------------
    # Decade
    # ------------------
    df["decade"] = df["year"].apply(lambda x: (x // 10) * 10 if pd.notna(x) else pd.NA)

    # ------------------
    # Transformaciones extra
    # ------------------
    if "duration_ms" in df.columns:
        df["duration_min"] = df["duration_ms"] / 60000  # milisegundos → minutos

    # ------------------
    # Drop lyrics
    # ------------------
    df = df.drop(columns=["lyrics"], errors="ignore")

    # ------------------
    # Drop columns que no aportan al análisis principal
    # ------------------
    if drop_columns:
        df = df.drop(columns=drop_columns, errors="ignore")

    return df
