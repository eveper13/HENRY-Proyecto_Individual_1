🎥 Sistema de Recomendación de Películas - Un Viaje hacia la Experiencia Cinematográfica Perfecta

Descripción del Proyecto
Este repositorio contiene el código y los archivos necesarios para desarrollar un sistema de recomendación de películas. El objetivo es construir un MVP que implemente un flujo completo de Machine Learning, desde el procesamiento y limpieza de datos hasta la creación de una API con FastAPI para consumir los datos y proporcionar recomendaciones. El proyecto aborda varios aspectos clave, como el ETL (Extract, Transform, Load), análisis exploratorio de datos (EDA), construcción de un modelo de recomendación y su implementación mediante una API.

Requerimientos del Proyecto
Este proyecto aborda los siguientes requerimientos principales:

Transformaciones de datos (ETL):

Desanidamiento de campos como belongs_to_collection, production_companies, entre otros.
... 

Desarrollo de la API:

Uso de FastAPI para crear 6 endpoints que permiten consultar información sobre las películas, actores y directores.
La API incluye funciones para devolver datos como el número de películas por mes, día, puntuación de títulos, votaciones, éxito de actores y directores, y recomendaciones basadas en similitud.

Análisis Exploratorio de Datos (EDA):
El EDA incluye análisis detallados de las variables, correlaciones, detección de outliers y patrones por género y país de producción. Algunas de las visualizaciones generadas incluyen:

Análisis de las relaciones entre variables mediante correlaciones.
Gráficos de correlación entre variables.
Distribución de puntuaciones y votaciones.
Nube de palabras de títulos más frecuentes.
Análisis de outliers en presupuesto y recaudación.
Identificación de patrones por género y país de producción.
Creación de una nube de palabras basada en los títulos de las películas.
Visualización de gráficos para obtener insights clave que preparan los datos para el sistema de recomendación.

Sistema de Recomendación
Creación de un modelo de recomendación de películas que sugiere títulos similares a la película ingresada.
Implementación de una función recomendacion(titulo) que devuelve una lista de 5 películas similares basadas en la puntuación de similitud.

El sistema de recomendación implementa un modelo que mide la similitud entre las películas basándose en características como género, país de producción y puntuaciones. 

Requisitos Técnicos
Python
FastAPI
Pandas, NumPy
Scikit-learn
Matplotlib, Seaborn (para visualización)
NLTK o similar (para la creación de la nube de palabras)
Render, Railway u otro servicio de deployment (para desplegar la API)

Estructura del Proyecto

├── Dataset_original/
│   ├── cast_credits.csv
│   ├── crew_credits.csv
│   ├── movies_dataset.csv
├── Dataset_procesados/
│   ├── credits_cast.parquet
│   ├── credits_crew.parquet
│   ├── movies_modificado.parquet
├── Notebooks/
│   ├── ETL.ipynb
│   ├── recomendacion.py
├── Reports/
│   ├── EDA.ipynb
│  
├── main.py
├── README.md
└── requirements.txt

Dataset_original/: Contiene los datasets utilizados en el proyecto.
Dataset_procesados: Contiene los datasets que se generaron en el proceso de ETL.
Notebooks/: Contiene los notebooks de Jupyter usados para el ETL y la funcion de recomendacion.py para usar en el main.py para el sistema de recomendacion de peliculas
Reports/: Contiene el notebook de Jupyter usados para el EDA
main.py: codigo de las funciones de fastapi solicitadas...
requirements.txt: Lista de dependencias del proyecto.

Autor
Desarrollado por Evelyn Perez.

