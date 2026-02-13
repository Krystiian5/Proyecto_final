#Tratamiento de datos
import pandas as pd

def eda_preliminar(df):
    """
    Realiza un análisis exploratorio preliminar sobre un DataFrame dado.

    Incluye:
    - Primeras filas del DataFrame (head)
    - Muestra aleatoria de 5 filas
    - Información general del DataFrame (tipo datos, nulos, etc)
    - Porcentaje de valores nulos por columna
    - Conteo de filas duplicadas
    - Distribución de valores para cada columna categórica (top 10)
    - Métricas de texto para columnas largas (lyrics)
    - Estadísticos numéricos

    Parameters:
    df (pd.DataFrame): DataFrame a analizar

    Returns:
    None
    """

    print("PRIMERAS FILAS DEL DATAFRAME")
    display(df.head())
    print('--------')

    print("MUESTRA ALEATORIA DE 5 FILAS")
    display(df.sample(5))
    print('--------')

    # Resumen de datos
    print('RESUMEN DE DATOS')
    print(f"Nuestro conjunto de datos presenta un total de {df.shape[0]} filas y {df.shape[1]} columnas")
    print('--------')

    # Tipos de datos
    print('INFO')
    columnas_por_tipo = {str(dtype): df.select_dtypes(include=[dtype]).columns.tolist()
                         for dtype in df.dtypes.unique()}

    print("Los tipos de las columnas son:")
    display(df.dtypes.to_frame(name="tipo_dato"))

    print("\nColumnas agrupadas por tipo de dato:")
    for tipo, columnas in columnas_por_tipo.items():
        print(f"- {tipo}: {columnas}")

    print("\n-----------------\n")
    
    # Columnas booleanas
    print("\nColumnas con posibles valores booleanos (0/1):")
    identificar_columnas_booleanas(df)
    print("\n-----------------\n")

    # Nulos
    print('NULOS')
    df_nulos = pd.DataFrame({
        "count": df.isnull().sum(),
        "% nulos": ((df.isnull().sum() / df.shape[0]) * 100).round(3)
    }).sort_values(by="% nulos", ascending=False)
    df_nulos = df_nulos[df_nulos["count"] > 0]
    print("Los nulos que tenemos en el conjunto de datos son:")
    display(df_nulos)
    print('--------')

    # Duplicados
    print('DUPLICADOS')
    if 'id' in df.columns:
        print(f"Duplicados considerando la columna 'id': {df.duplicated(subset='id').sum()}")
    else:
        print(f"No se encontró la columna 'id', duplicados totales: {df.duplicated().sum()}")
    print('--------')

    # Frecuencia categóricas (top 10) y métricas de texto
    print('FRECUENCIA CATEGORICAS')
    for col in df.select_dtypes(include='O').columns:
        if df[col].apply(lambda x: isinstance(x, str) and len(x) > 100).mean() > 0.5:
            print(f"{col.upper()} - Columna de texto larga, se muestra métricas simples")
            print(f"Longitud media de texto: {df[col].dropna().apply(len).mean():.2f}")
            print(f"Número de palabras promedio: {df[col].dropna().apply(lambda x: len(x.split())).mean():.2f}")
            print('-------')
            continue
        print(col.upper())
        print(df[col].value_counts().head(10))  # top 10 valores
        print('-------')

    # Estadísticos numéricos
    print('ESTADISTICOS NUMERICOS')
    display(df.describe().T.round(2))


def identificar_columnas_booleanas(df):
    """
    Identifica columnas con valores booleanos (0/1)
    """
    posibles_booleanos = [col for col in df.columns if set(df[col].dropna().unique()) <= {0,1}]
    print(f"Columnas que podrían ser booleanas: {posibles_booleanos}")
    return posibles_booleanos
