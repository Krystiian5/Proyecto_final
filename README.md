# Spotify Songs & Artists – Exploratory Data Analysis and Dashboard

## 📌 Introducción

Este proyecto consiste en un **Análisis Exploratorio de Datos (EDA)** realizado con Python sobre dos conjuntos de datos relacionados con **canciones y artistas de Spotify**.

El análisis integra información sobre características musicales, popularidad de las canciones, géneros y métricas asociadas a los artistas, con el objetivo de **identificar patrones y relaciones entre las características de las canciones, los artistas y su popularidad**.

El proyecto se desarrolla como parte del **proyecto final**, aplicando técnicas de exploración, limpieza, transformación, integración y análisis de datos, finalizando con la creación de un **dataset final integrado**, un **informe explicativo** y un **dashboard interactivo desarrollado en Excel**.

---

## ✅ Requisitos del proyecto

El desarrollo del proyecto contempla los siguientes puntos:

- Transformación y limpieza profunda de los datos
- Análisis exploratorio y estadístico descriptivo
- Visualización de la información
- Integración de múltiples fuentes de datos
- Elaboración de un informe explicativo del análisis
- Desarrollo de un dashboard que aporte valor

---

## 🛠️ Herramientas utilizadas

Además de las librerías base de Python, el proyecto hace uso de herramientas orientadas a mantener un flujo de trabajo organizado y reproducible:

- **Python**
- **Pandas** – Manipulación y análisis de datos
- **NumPy** – Operaciones numéricas
- **Matplotlib y Seaborn** – Visualización de datos
- **Visual Studio Code** – Desarrollo del proyecto
- **Jupyter Notebooks** – Análisis exploratorio
- **Excel** – Dashboard
- **GitHub** – Control de versiones

---

## 📂 Estructura del repositorio

```
Proyecto_final/
├── README.md
├── Informe_explicativo.pdf
│
├── data/
│   ├── raw/
│   │   ├── artists.csv
│   │   └── songs.csv
│   │
│   └── processed/
│   │   ├── songs_clean.csv
│   │   └── artists_clean.csv
│   │   └── music_dataset.csv
│
├── notebooks/
│   ├── 01.songs_exploracion.ipynb
│   └── 02.songs_limpieza.ipynb
│   └── 03.artists_exploracion.ipynb
│   └── 04.artists_limpieza.ipynb
│   └── 05.merge_datasets.ipynb
│   └── 06.music_eda.ipynb
│
├── dashboard/
│   └── Music_Analytics_Dashboard.xlsx
│
└── src/
    └── soporte_exploracion.py
    └── soporte_limpieza.py
    └── soporte_merge.py
    └── soporte_visualizacion.py
```

---

## 📁 Código de soporte

Para facilitar la reutilización del código y evitar tareas repetitivas, se desarrollaron diferentes módulos de soporte en la carpeta `src/`:

- `soporte_exploracion.py` – Funciones para la exploración y análisis inicial de los datos.
- `soporte_limpieza.py` – Funciones para la limpieza y transformación de los datasets.
- `soporte_merge.py` – Funciones utilizadas en la integración de las diferentes fuentes.
- `soporte_visualizacion.py` – Funciones reutilizables para la generación de visualizaciones.

---
## 📊 Conjuntos de datos

Los datos utilizados en el proyecto proceden del dataset público de Kaggle:

🔗 [550K Spotify Songs – Audio, Lyrics and Genres](https://www.kaggle.com/datasets/serkantysz/550k-spotify-songs-audio-lyrics-and-genres/data)

A partir de este recurso se trabajó con dos fuentes principales:

- `songs.csv` – Información sobre canciones, incluyendo características musicales, popularidad, género, año, artistas y colaboraciones.
- `artists.csv` – Información sobre artistas, incluyendo géneros, seguidores y popularidad.

Ambos datasets fueron limpiados y posteriormente integrados para crear un **dataset final enriquecido**, utilizado como base para el EDA y el dashboard.

---
## 🔍 Exploración, limpieza e integración

El proyecto comienza con una exploración independiente de los datasets de canciones y artistas, analizando su estructura, tipos de datos, valores nulos, duplicados, distribuciones y estadísticos descriptivos.

Posteriormente se realiza la limpieza y transformación de los datos, incluyendo el tratamiento de valores nulos, conversión de tipos, estandarización de variables y creación de nuevas variables derivadas.

También se revisaron posibles **duplicados lógicos de canciones**, comprobando aquellos registros que compartían información como título, álbum y artista antes de tomar decisiones sobre su tratamiento.

Una vez finalizada la limpieza, ambos datasets se integran mediante los identificadores disponibles, obteniendo un dataset final que combina información sobre:

- Características musicales
- Popularidad de las canciones
- Géneros
- Artistas
- Seguidores y popularidad de los artistas
- Colaboraciones
- Décadas
- Duración de las canciones

---

## 📈 Análisis exploratorio descriptivo (EDA)

El EDA final se centra en analizar la **popularidad de las canciones** y su relación con diferentes factores.

Los principales análisis realizados estudian:

- Popularidad media por género.
- Evolución de la popularidad por década.
- Relación entre seguidores del artista y popularidad de sus canciones.
- Popularidad media según tramos de seguidores.
- Relación entre duración y popularidad.
- Diferencias entre canciones con y sin colaboración.
- Características musicales del 10% de canciones más populares frente al conjunto del dataset.
- Correlaciones entre la popularidad y diferentes variables numéricas.
---

## 📊 Visualizaciones clave

Entre las principales visualizaciones desarrolladas durante el EDA destacan:

- **Popularidad media por género**
- **Evolución de la popularidad media por década**
- **Top 10 artistas según número de seguidores**
- **Características musicales del 10% más popular frente al dataset completo**
- **Popularidad media por tramo de seguidores**
- **Popularidad media por tramo de duración**

Estas visualizaciones permiten analizar la popularidad desde diferentes perspectivas y sirven como base para las conclusiones obtenidas.

---
## 📊 Dashboard

Como resultado final se desarrolló un **dashboard interactivo en Excel** que resume los principales resultados del EDA.

El dashboard incluye:

- KPIs con las principales métricas del análisis.
- Segmentadores interactivos.
- Gráficos relacionados con género, evolución temporal, artistas y características de las canciones.

Las conexiones entre los segmentadores y los diferentes elementos se definieron teniendo en cuenta la lógica de cada análisis.
---

## 🧠 Principales conclusiones

Los resultados obtenidos muestran que la popularidad de una canción no puede explicarse mediante un único factor.

Entre las principales conclusiones destacan:

- Existen diferencias de popularidad media entre géneros y décadas.
- Un mayor número de seguidores del artista no garantiza una mayor popularidad de sus canciones.
- Los factores relacionados con el artista y el contexto presentan una relación más clara con la popularidad que las características musicales analizadas individualmente.
- Las canciones del 10% más popular presentan algunas diferencias en determinadas características musicales, especialmente en bailabilidad y *valence*, aunque estas diferencias son moderadas.
- En conjunto, la popularidad parece estar relacionada con una combinación de factores asociados al artista, el contexto temporal y las características de la propia canción.

---
## ⚠️ Limitaciones del análisis

El análisis es de carácter exploratorio, por lo que permite identificar **patrones y relaciones**, pero no establecer relaciones de causalidad.

Además, la popularidad puede estar influida por factores no disponibles en los datos analizados, como campañas de marketing, presencia en redes sociales, inclusión en playlists o tendencias culturales.

Por ello, las conclusiones deben interpretarse como relaciones observadas dentro del dataset y no como una explicación definitiva de los factores que determinan el éxito de una canción.

---

## 📄 Documentación adicional

El repositorio incluye un **informe explicativo** con información detallada sobre la metodología, el proceso de limpieza y transformación, el análisis exploratorio, los resultados y las conclusiones finales.

📎 **Informe explicativo:** `Informe_explicativo.pdf`