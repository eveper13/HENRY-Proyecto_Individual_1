

![Hora de Pelis](img/movies.webp)



### 🎥Sistema de Recomendación de Películas

**¿Alguna vez te has sentido perdido entre miles de opciones de películas, sin saber cuál elegir?**  
Este proyecto es la solución perfecta: un sistema de recomendación de películas diseñado para entender tus gustos y sugerirte títulos que disfrutarás.

En este repositorio, encontrarás todo lo necesario para desarrollar un Sistema de Recomendación de Películas. Desde la limpieza y transformación de datos hasta la implementación de un modelo de recomendación y el desarrollo de una API que puedes consultar desde cualquier lugar. Este proyecto es un viaje completo a través del Machine Learning y el análisis de datos.

## ¿Qué Puedes Esperar?

- **Transformaciones de Datos (ETL):**  
  Aprende a desanidar y procesar datos complejos, gestionando valores nulos y duplicados, para prepararlos para un análisis exhaustivo.
  
- **Análisis Exploratorio de Datos (EDA):**  
  Descubre correlaciones sorprendentes y patrones ocultos que dictan el éxito en la taquilla, con visualizaciones atractivas que te ofrecen una nueva perspectiva del mundo cinematográfico.
  
- **Recomendaciones Personalizadas:**  
  Implementa un modelo de recomendación basado en la similitud de puntuación, que selecciona las 5 películas que más se alinean con tus gustos.

---

## Tecnologías Usadas

- **Python:** La base de todo el proyecto, poderosa y versátil.
- **FastAPI:** Creación de una API rápida y eficiente, lista para manejar consultas complejas.
- **Pandas, NumPy:** Manipulación y análisis de datos en su máxima expresión.
- **Scikit-learn:** Implementación de la similitud coseno para recomendaciones precisas.
- **Matplotlib, Seaborn:** Visualizaciones que convierten números en historias.
- **NLTK:** Análisis de texto para extraer temas populares de los títulos cinematográficos.
- **Render:** Despliegue de la API para accederla desde cualquier lugar.

---

## Desarrollo de la API

El poder de la personalización: Hemos creado 6 endpoints que no solo proporcionan datos, sino que también cuentan historias.

### Endpoints Claves:

- **Descubre los mejores meses y días para los estrenos:**  
  Analiza el calendario de lanzamientos para identificar las fechas más populares.
  
- **Conoce a los directores y actoresmás exitosos:**  
  Averigua cuáles han tenido la mejor racha de éxitos.
  
- **Obtén recomendaciones personalizadas:**  
  Basadas en tus preferencias y en un análisis de similitud (con recomendacion de 5 peliculas).
  
- **Verifica la popularidad y año de estreno de tus películas favoritas**

  
  Todo desde un solo lugar.


  
![sistema de recomendacion](img/sistema-de-recomendacion.png)



Puedes ver y probar la API en este enlace: [Render - FastAPI](https://henry-proyecto-individual-1-du8k.onrender.com/docs).

---

## Estructura del Proyecto

```scss
├── [Dataset_original/](./Dataset_original/)
│   ├── [cast_credits.csv](./Dataset_original/cast_credits.csv)
│   ├── [crew_credits.csv](./Dataset_original/crew_credits.csv)
│   ├── [movies_dataset.csv](./Dataset_original/movies_dataset.csv)
├── [Dataset_procesados/](./Dataset_procesados/)
│   ├── [credits_cast.parquet](./Dataset_procesados/credits_cast.parquet)
│   ├── [credits_crew.parquet](./Dataset_procesados/credits_crew.parquet)
│   ├── [movies_modificado.parquet](./Dataset_procesados/movies_modificado.parquet)
├── [Notebooks/](./Notebooks/)
│   ├── [ETL.ipynb](./Notebooks/ETL.ipynb)
│   ├── [recomendacion.py](./Notebooks/recomendacion.py)
├── [Reports/](./Reports/)
│   ├── [EDA.ipynb](./Reports/EDA.ipynb)
├── [main.py](./main.py)
├── [README.md](./README.md)
└── [requirements.txt](./requirements.txt)


Dataset_original/: Datos en bruto, listos para ser transformados.
Dataset_procesados/: Resultados del ETL, datos limpios y listos para análisis.
Notebooks/: Donde se realiza la magia del ETL y las recomendaciones.
Reports/: Visualizaciones e insights descubiertos en el EDA.
main.py: Corazón de la API, donde se implementa el sistema de recomendación.
README.md: Esta guía que estás leyendo.
requirements.txt: Herramientas necesarias para ejecutar el proyecto.


Autor
Este proyecto fue desarrollado por Evelyn Perez.

¡Explora, contribuye y disfruta de tu experiencia cinematográfica personalizada!


Video Explicativo:
Puedes ver una explicación completa del proyecto en este video.