# ==========================================
# SOPORTE VISUALIZACIÓN
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def _set_title(ax, title, default):
    """
    Establece un título personalizado si se proporciona.
    En caso contrario utiliza el título por defecto.
    """
    ax.set_title(title if title else default)


def _save_figure(save_path):
    """
    Guarda la figura actual si se proporciona una ruta.
    """
    if save_path:
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

# ==========================================
# RESUMEN DEL DATASET
# ==========================================

def dataset_summary(df):
    """
    Muestra un resumen general del DataFrame.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame a analizar.

    Devuelve
    --------
    None
    """

    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    print(f"\nNúmero de filas: {df.shape[0]:,}")
    print(f"Número de columnas: {df.shape[1]}")
    print(f"Número de duplicados: {df.duplicated().sum():,}")
    print(f"Memoria utilizada: {df.memory_usage(deep=True).sum()/1024**2:.2f} MB")

    print("\nTipos de datos:")

    display(
        pd.DataFrame(
            {
                "Tipo": df.dtypes,
                "Nulos": df.isna().sum(),
                "% Nulos": (
                    df.isna().mean() * 100
                ).round(2)
            }
        )
    )


# ==========================================
# VALORES NULOS
# ==========================================

def missing_values(df):
    """
    Devuelve una tabla con el número y porcentaje
    de valores nulos por columna.

    Parámetros
    ----------
    df : pandas.DataFrame

    Devuelve
    --------
    pandas.DataFrame
    """

    missing = pd.DataFrame(
        {
            "Missing": df.isna().sum(),
            "Percentage": (
                df.isna().mean() * 100
            ).round(2)
        }
    )

    missing = (
        missing
        .sort_values(
            by="Missing",
            ascending=False
        )
    )

    return missing


# ==========================================
# RESUMEN VARIABLES NUMÉRICAS
# ==========================================

def numeric_summary(df):
    """
    Devuelve estadísticas descriptivas de todas
    las variables numéricas.
    """

    numeric = df.select_dtypes(
        include="number"
    )

    summary = (
        numeric
        .describe()
        .T
    )

    summary["median"] = numeric.median()

    summary["iqr"] = (
        numeric.quantile(0.75)
        - numeric.quantile(0.25)
    )

    summary["missing"] = numeric.isna().sum()

    summary["missing_%"] = (
        numeric.isna().mean() * 100
    ).round(2)

    # Redondear todas las columnas numéricas
    summary = summary.round(3)

    return summary


# ==========================================
# VARIABLES CATEGÓRICAS
# ==========================================

def categorical_summary(df):
    """
    Resume todas las variables categóricas.

    Parámetros
    ----------
    df : pandas.DataFrame

    Devuelve
    --------
    pandas.DataFrame
    """

    categorical = df.select_dtypes(
        include=["object", "category", "string"]
    )

    summary = pd.DataFrame({

        "Unique values":
        categorical.nunique(),

        "Missing":
        categorical.isna().sum(),

        "Most frequent":
        categorical.mode().iloc[0],

        "Frequency":
        categorical.apply(
            lambda x: x.value_counts().iloc[0]
            if not x.value_counts().empty
            else None
        )

    })

    return summary
# ==========================================
# TABLA DE FRECUENCIAS
# ==========================================

def frequency_table(
    df,
    column,
    top_n=None,
    sort=True
):
    """
    Devuelve una tabla de frecuencias de una variable categórica.

    Parámetros
    ----------
    df : pandas.DataFrame

    column : str

    top_n : int o None
        Número máximo de categorías a mostrar.

    sort : bool
        Si True ordena por frecuencia descendente.

    Devuelve
    --------
    pandas.DataFrame
    """

    table = pd.DataFrame({

        "Frequency":
        df[column].value_counts(dropna=False),

        "Percentage":
        (
            df[column]
            .value_counts(dropna=False, normalize=True)
            * 100
        ).round(2)

    })

    table = table.reset_index()

    table.columns = [
        column,
        "Frequency",
        "Percentage"
    ]

    if sort:
        table = table.sort_values(
            by="Frequency",
            ascending=False
        )

    if top_n is not None:
        table = table.head(top_n)

    return table
# ==========================================
# DUPLICADOS
# ==========================================

def duplicated_rows(df, subset=None):
    """
    Muestra el número y porcentaje de filas duplicadas.

    Parámetros
    ----------
    df : pandas.DataFrame

    subset : str, list o None, opcional
        Columna o columnas sobre las que comprobar duplicados.
        Si es None se utilizan todas las columnas.

    Devuelve
    --------
    int
        Número de filas duplicadas.
    """

    duplicates = df.duplicated(subset=subset).sum()

    percentage = round(
        duplicates / len(df) * 100,
        2
    )

    print("=" * 60)
    print("DUPLICATED ROWS")
    print("=" * 60)

    if subset is None:
        print("Columns: All")
    else:
        print(f"Columns: {subset}")

    print(f"Duplicated rows: {duplicates}")
    print(f"Percentage: {percentage}%")

    return duplicates


# ==========================================
# HISTOGRAMA
# ==========================================

def histogram(
    df,
    column,
    bins=30,
    kde=False,
    figsize=(10, 6),
    color="steelblue",
    title=None,
    save_path=None
):
    """
    Dibuja un histograma de una variable numérica.

    Parámetros
    ----------
    df : pandas.DataFrame

    column : str

    bins : int

    kde : bool

    figsize : tuple

    color : str

    title : str o None

    save_path : str o None
    """

    fig, ax = plt.subplots(figsize=figsize)

    sns.histplot(
        data=df,
        x=column,
        bins=bins,
        kde=kde,
        color=color,
        edgecolor="black",
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"Distribution of {column}"
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    plt.tight_layout()

    _save_figure(save_path)
    plt.show()
    return ax
# ==========================================
# HISTOGRAMAS EN CUADRÍCULA
# ==========================================

def histograms_grid(
    df,
    columns,
    cols=2,
    bins=30,
    kde=False,
    figsize=(14, 8),
    color="steelblue",
    save_path=None
):
    """
    Representa varios histogramas en una cuadrícula.

    Parámetros
    ----------
    df : pandas.DataFrame

    columns : list
        Lista de variables numéricas.

    cols : int
        Número de columnas de la cuadrícula.

    bins : int

    kde : bool

    figsize : tuple

    color : str

    save_path : str o None
    """

    import math

    rows = math.ceil(len(columns) / cols)

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=figsize
    )

    axes = axes.flatten()

    for ax, column in zip(axes, columns):

        sns.histplot(
            data=df,
            x=column,
            bins=bins,
            kde=kde,
            color=color,
            edgecolor="black",
            ax=ax
        )

        ax.set_title(column)

    for ax in axes[len(columns):]:
        ax.remove()

    plt.tight_layout()

    _save_figure(save_path)


# ==========================================
# BOXPLOT
# ==========================================

def boxplot(
    df,
    column,
    figsize=(8, 4),
    color="skyblue",
    showfliers=False,
    title=None,
    save_path=None
):
    """
    Dibuja un boxplot de una variable numérica.
    """

    fig, ax = plt.subplots(figsize=figsize)

    sns.boxplot(
        x=df[column],
        color=color,
        showfliers=showfliers,
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"Boxplot of {column}"
    )

    plt.tight_layout()

    _save_figure(save_path)

    plt.show()
    return ax
# ==========================================
# BOXPLOTS EN CUADRÍCULA
# ==========================================

def boxplots_grid(
    df,
    columns,
    cols=2,
    figsize=(14, 8),
    color="skyblue",
    showfliers=False,
    save_path=None
):
    """
    Representa varios boxplots en una cuadrícula.

    Parámetros
    ----------
    df : pandas.DataFrame

    columns : list
        Variables numéricas.

    cols : int

    figsize : tuple
    """

    import math

    rows = math.ceil(len(columns) / cols)

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=figsize
    )

    axes = axes.flatten()

    for ax, column in zip(axes, columns):

        sns.boxplot(
            x=df[column],
            color=color,
            showfliers=showfliers,
            ax=ax
        )

        ax.set_title(column)

    for ax in axes[len(columns):]:
        ax.remove()

    plt.tight_layout()

    _save_figure(save_path)

# ==========================================
# COUNTPLOT
# ==========================================

def countplot(
    df,
    column,
    figsize=(10, 6),
    rotation=45,
    palette="Blues_r",
    title=None,
    save_path=None
):
    """
    Representa todas las categorías de una variable categórica.

    Parámetros
    ----------
    df : pandas.DataFrame

    column : str
        Variable categórica.
    """

    fig, ax = plt.subplots(figsize=figsize)

    sns.countplot(
        data=df,
        x=column,
        order=df[column].value_counts().index,
        hue=column,
        palette=palette,
        legend=False,
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"Distribution of {column}"
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Count")

    plt.xticks(rotation=rotation)

    plt.tight_layout()

    _save_figure(save_path)

    plt.show()

    return ax
# ==========================================
# COUNTPLOT TOP N
# ==========================================

def countplot_top(
    df,
    column,
    top_n=10,
    normalize=False,
    figsize=(10, 6),
    rotation=45,
    palette="Blues_r",
    title=None,
    save_path=None
):
    """
    Representa las categorías más frecuentes.

    Parámetros
    ----------
    df : pandas.DataFrame

    column : str

    top_n : int

    normalize : bool
        Si True representa porcentajes.
    """

    counts = (
        df[column]
        .value_counts(normalize=normalize)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=figsize)

    sns.barplot(
        x=counts.index,
        y=counts.values,
        hue=counts.index,
        palette=palette,
        legend=False,
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"Top {top_n} values of {column}"
    )

    ax.set_xlabel(column)

    if normalize:
        ax.set_ylabel("Percentage")
    else:
        ax.set_ylabel("Count")

    plt.xticks(rotation=rotation)

    plt.tight_layout()

    _save_figure(save_path)
    plt.show()

    return ax

# ==========================================
# PIE CHART
# ==========================================

def piechart(
    df,
    column,
    top_n=None,
    figsize=(7, 7),
    autopct="%1.1f%%",
    title=None,
    save_path=None
):
    """
    Representa un gráfico de sectores de una variable categórica.

    Parámetros
    ----------
    df : pandas.DataFrame

    column : str

    top_n : int o None
    """

    counts = df[column].value_counts()

    if top_n is not None:
        counts = counts.head(top_n)

    fig, ax = plt.subplots(figsize=figsize)

    ax.pie(
        counts.values,
        labels=counts.index,
        autopct=autopct,
        startangle=90
    )

    _set_title(
        ax,
        title,
        f"Distribution of {column}"
    )

    ax.axis("equal")

    plt.tight_layout()

    _save_figure(save_path)
    plt.show()

    return ax
# ==========================================
# GROUPED BARPLOT
# ==========================================

def grouped_barplot(
    df,
    groupby,
    value,
    agg="mean",
    sort=True,
    ascending=False,
    top_n=None,
    decimals=2,
    figsize=(10,6),
    rotation=45,
    palette="viridis",
    title=None,
    save_path=None
):
    """
    Representa un barplot de una variable agregada
    por una variable categórica.

    Parámetros
    ----------
    df : pandas.DataFrame

    groupby : str
        Variable categórica.

    value : str
        Variable numérica.

    agg : str
        Función de agregación:
        "mean", "median", "sum",
        "count", "max" o "min".

    sort : bool
        Ordenar los resultados.

    ascending : bool
        Orden ascendente.

    top_n : int o None

    decimals : int
    """

    data = (
        df
        .groupby(groupby)[value]
        .agg(agg)
        .round(decimals)
    )

    if sort:
        data = data.sort_values(
            ascending=ascending
        )

    if top_n is not None:
        data = data.head(top_n)

    fig, ax = plt.subplots(figsize=figsize)

    sns.barplot(
        x=data.index,
        y=data.values,
        hue=data.index,
        palette=palette,
        legend=False,
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"{agg.capitalize()} {value} by {groupby}"
    )

    ax.set_xlabel(groupby)
    ax.set_ylabel(f"{agg.capitalize()} {value}")

    plt.xticks(rotation=rotation)

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt=f"%.{decimals}f",
            padding=3,
            fontsize=9
        )

    plt.tight_layout()

    _save_figure(save_path)

    plt.show()

# ==========================================
# VIOLINPLOT
# ==========================================

def violinplot(
    df,
    x,
    y,
    figsize=(10, 6),
    palette="viridis",
    rotation=45,
    title=None,
    save_path=None
):
    """
    Representa un violinplot para comparar la distribución
    de una variable numérica entre categorías.

    Parámetros
    ----------
    df : pandas.DataFrame

    x : str
        Variable categórica.

    y : str
        Variable numérica.
    """

    fig, ax = plt.subplots(figsize=figsize)

    sns.violinplot(
        data=df,
        x=x,
        y=y,
        hue=x,
        palette=palette,
        legend=False,
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"{y} by {x}"
    )

    plt.xticks(rotation=rotation)

    plt.tight_layout()

    _save_figure(save_path)
    plt.show()

    return ax


# ==========================================
# SCATTERPLOT
# ==========================================

def scatterplot(
    df,
    x,
    y,
    hue=None,
    alpha=0.6,
    figsize=(8, 6),
    title=None,
    save_path=None
):
    """
    Representa un diagrama de dispersión.
    """

    fig, ax = plt.subplots(figsize=figsize)

    sns.scatterplot(
        data=df,
        x=x,
        y=y,
        hue=hue,
        alpha=alpha,
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"{y} vs {x}"
    )

    plt.tight_layout()

    _save_figure(save_path)
    plt.show()

    return ax

# ==========================================
# REGPLOT
# ==========================================

def regplot(
    df,
    x,
    y,
    figsize=(8, 6),
    scatter_alpha=0.3,
    scatter_size=20,
    line_color="red",
    title=None,
    save_path=None
):
    """
    Representa un gráfico de dispersión con línea de regresión.

    Parámetros
    ----------
    df : pandas.DataFrame

    x : str
        Variable del eje X.

    y : str
        Variable del eje Y.

    figsize : tuple
        Tamaño de la figura.

    scatter_alpha : float
        Transparencia de los puntos.

    scatter_size : int
        Tamaño de los puntos.

    line_color : str
        Color de la línea de regresión.

    title : str o None

    save_path : str o None
    """

    fig, ax = plt.subplots(figsize=figsize)

    sns.regplot(
        data=df,
        x=x,
        y=y,
        scatter_kws={
            "alpha": scatter_alpha,
            "s": scatter_size
        },
        line_kws={
            "color": line_color
        },
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"{y} vs {x}"
    )

    plt.tight_layout()

    _save_figure(save_path)

    plt.show()

# ==========================================
# LINEPLOT
# ==========================================

def lineplot(
    df,
    x,
    y,
    figsize=(10, 6),
    marker="o",
    title=None,
    save_path=None
):
    """
    Representa una gráfica de líneas.
    """

    fig, ax = plt.subplots(figsize=figsize)

    sns.lineplot(
        data=df,
        x=x,
        y=y,
        marker=marker,
        ax=ax
    )

    _set_title(
        ax,
        title,
        f"{y} by {x}"
    )

    plt.tight_layout()

    _save_figure(save_path)
    plt.show()

    return ax


# ==========================================
# CORRELATION HEATMAP
# ==========================================

def correlation_heatmap(
    df,
    columns=None,
    figsize=(12, 8),
    cmap="coolwarm",
    annot=False,
    save_path=None
):
    """
    Representa el mapa de calor de correlaciones.

    Parámetros
    ----------
    df : pandas.DataFrame

    columns : list o None
        Lista de variables numéricas a incluir.
        Si es None, utiliza todas las variables numéricas.

    figsize : tuple
        Tamaño de la figura.

    cmap : str
        Paleta de colores.

    annot : bool
        Mostrar coeficientes de correlación.

    save_path : str o None
        Ruta donde guardar la figura.
    """

    if columns is not None:
        corr = df[columns].corr(numeric_only=True)
    else:
        corr = (
            df
            .select_dtypes(include="number")
            .corr(numeric_only=True)
        )

    fig, ax = plt.subplots(figsize=figsize)

    sns.heatmap(
        corr,
        cmap=cmap,
        annot=annot,
        fmt=".2f",
        ax=ax
    )

    ax.set_title("Correlation Heatmap")

    plt.tight_layout()

    _save_figure(save_path)

    plt.show()

    return ax

# ==========================================
# TABLA DE CORRELACIONES
# ==========================================

def correlation_table(
    df,
    target=None
):
    """
    Devuelve la matriz de correlaciones o las
    correlaciones respecto a una variable.

    Parámetros
    ----------
    df : pandas.DataFrame

    target : str o None
    """

    if target is None:
        return corr

    return (
        corr[target]
        .drop(target)
        .sort_values(ascending=False)
)

# ==========================================
# CORRELATION VALUE
# ==========================================

def correlation_value(
    df,
    x,
    y,
    method="pearson"
):
    """
    Calcula la correlación entre dos variables numéricas.

    Parámetros
    ----------
    df : pandas.DataFrame

    x : str
        Variable del eje X.

    y : str
        Variable del eje Y.

    method : str, default="pearson"
        Método de correlación:
        - "pearson"
        - "spearman"
        - "kendall"

    Devuelve
    --------
    float
        Valor de la correlación.
    """

    corr = df[x].corr(df[y], method=method)

    print(f"{method.capitalize()} correlation: {corr:.3f}")

    return corr
# ==========================================
# PAIRPLOT
# ==========================================

def pairplot(
    df,
    columns,
    hue=None
):
    """
    Representa un pairplot de las variables seleccionadas.

    Parámetros
    ----------
    df : pandas.DataFrame

    columns : list

    hue : str o None
    """

    variables = columns.copy()

    if hue is not None and hue not in variables:
        variables.append(hue)

    sns.pairplot(
        data=df[variables],
        hue=hue
    )

    plt.show()