from fastapi import FastAPI
import pandas as pd
from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Notebooks.recomendacion import recomendar_peliculas_por_similitud  # Importar la función de recomendación


app = FastAPI()

# Cargar el dataset
movies = pd.read_parquet("Dataset_procesados/movies_modificado.parquet")  
crew_df = pd.read_parquet("Dataset_procesados/credits_crew.parquet") 
cast_df = pd.read_parquet("Dataset_procesados/credits_cast.parquet") 

 #Crear el vectorizador y ajustar al dataset
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies['overview'].fillna(''))

# Convertir las fechas si no lo has hecho aún
movies['fecha_lanzamiento'] = pd.to_datetime(movies['release_date'], errors='coerce')

# 1. Función para cantidad de filmaciones por mes
@app.get("/cantidad_filmaciones_mes/{mes}", description="Consulta la cantidad de películas estrenadas en un mes específico. Ejemplo de ingreso: enero",
         operation_id="obtener_cantidad_filmaciones_por_mes"
          )
def cantidad_filmaciones_mes(mes: str):
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes_num = meses.get(mes.lower())
    if mes_num:
        cantidad = movies[movies['fecha_lanzamiento'].dt.month == mes_num].shape[0]
        return f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}."
    else:
        return "Mes no válido. Por favor, ingrese un mes en español, por ejemplo: Octubre."

# 2. Función para cantidad de filmaciones por día
@app.get("/cantidad_filmaciones_dia/{dia}", description="Consulta la cantidad de películas estrenadas en un día específico. Ejemplo de ingreso: martes", 
         operation_id="obtener_cantidad_filmaciones_por_dia"
         )
def cantidad_filmaciones_dia(dia: str):
    dias = {
        "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "domingo": 6
    }
    # Convertir el día a minúsculas para que no distinga entre mayúsculas y minúsculas
    dia_num = dias.get(dia.lower())
    
    if dia_num is not None:
        cantidad = movies[movies['fecha_lanzamiento'].dt.weekday == dia_num].shape[0]
        return f"{cantidad} películas fueron estrenadas en los días {dia.capitalize()}."
    else:
        return "Día no válido. Por favor, ingrese un día en español, por ejemplo: martes."


# 3. Función para obtener el score por título
@app.get("/score_titulo/{titulo}", operation_id="obtener año y puntaje de peliculas")
def score_titulo(titulo: str):
    """
    Se ingresa el título de una filmación esperando como respuesta el título
    Parámetros:
    - `Titulo`: Titulo de la pelicula (Ejemplo: "Toy Story")

    Retorna:
    - El titulo de la filmacion.
    - Año de estreno de la película
    - Puntaje (score/popularidad) de la pelicula
    """
    film = movies[movies['title'].str.lower() == titulo.lower()]
    if not film.empty:
        titulo = film.iloc[0]['title']
        año = film.iloc[0]['release_year']
        score = film.iloc[0]['popularity']
        return f"La película {titulo} fue estrenada en el año {año} con un score/popularidad de {score}."
    else:
        return "Película no encontrada."

# 4. Función para obtener los votos por título
@app.get("/votos_titulo/{titulo}", operation_id="obtener promedio de votos por pelicula")
def votos_titulo(titulo: str):
    """
    Se ingresa el título de una filmación esperando como respuesta el título
    Parámetros:
    - `Titulo`: Titulo de la pelicula (Ejemplo: "Jumanji")

    Retorna:
    - El titulo de la filmacion.
    - La cantidad de votos de las película
    - El valor promedio de las votaciones.
    """
    film = movies[movies['title'].str.lower() == titulo.lower()]
    if not film.empty:
        votos = film.iloc[0]['vote_count']
        promedio_votos = film.iloc[0]['vote_average']
        if votos >= 2000:
            return f"La película {titulo} cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}."
        else:
            return "La película no tiene suficientes valoraciones (menos de 2000)."
    else:
        return "Película no encontrada."
    

# 6. Función para obtener informacion sobre el Actor
@app.get("/actor/{nombre_actor}", operation_id="obtener detalles del Actor")
def get_actor(nombre_actor: str):
    """
    Busca información sobre el éxito de un actor en base al nombre proporcionado.

    Ejemplo de uso:
    - URL: /actor/TomHanks
    
    Parámetros:
    - `nombre_actor`: Nombre del actor (Ejemplo: "Tom Hanks")

    Retorna:
    - Número de películas en las que el actor ha participado.
    - Retorno total de las películas.
    - Promedio de retorno por película.
    """
    # Convertir a minúsculas para búsqueda insensible a mayúsculas
    nombre_actor_normalizado = nombre_actor.lower()  # o nombre_actor.casefold()

    # Filtrar el dataset cast por el nombre del actor (también insensible a mayúsculas)
    actor_films = cast_df[cast_df['name_actor'].str.lower() == nombre_actor_normalizado]
    
    if actor_films.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado")

    # Obtener las películas en las que ha participado
    num_peliculas = actor_films.shape[0]
    
    # Unir con el dataset de movies para obtener el retorno
    actor_movies = pd.merge(actor_films, movies, left_on='idMovies', right_on='idMovies')
    
    # Verificar si hay información de ingresos en las películas
    if 'revenue' not in actor_movies.columns:
        raise HTTPException(status_code=500, detail="La información de ingresos no está disponible en el dataset de películas.")

    # Calcular el retorno total y el promedio
    retorno_total = actor_movies['revenue'].sum()
    promedio_retorno = retorno_total / num_peliculas if num_peliculas > 0 else 0
    
    return {
        "actor": nombre_actor,
        "numero_peliculas": num_peliculas,
        "retorno_total": retorno_total,
        "promedio_retorno": promedio_retorno
    }


# 6. Función para obtener informacion sobre el Director
@app.get("/director/{nombre_director}", operation_id="obtener_peliculas_por_director")
def get_director(nombre_director: str):
    """
    Description="Este endpoint devuelve las películas dirigidas por el director especificado y su éxito promedio basado en el retorno de inversión.
    Parámetros:
    - `nombre_director`: Nombre del director (Ejemplo: "Steven Spielberg")

    Retorna:
    - Mensaje descriptivo.
    - Éxito promedio basado en el retorno de inversión.
    - Lista de películas con detalles como el título, fecha de lanzamiento, retorno, costo y ganancia.

    Ejemplo de uso:
    Realiza una solicitud GET a `/director/{nombre_director}` con el parámetro `nombre_director=Steven%20Spielberg`.
    """
    
    # Normalizar el nombre del director a minúsculas
    nombre_director_normalizado = nombre_director.lower()

    # Filtrar el dataset de crew para obtener las películas del director especificado (en minúsculas)
    director_movies = crew_df[
        (crew_df['crew_name'].str.lower() == nombre_director_normalizado) & 
        (crew_df['crew_job'] == 'Director')
        ]
        
    if director_movies.empty:
        raise HTTPException(status_code=404, detail="Director no encontrado. Asegúrate de que el nombre esté escrito correctamente y que el director haya dirigido al menos una película en la base de datos.")
        
    # Unir con el dataset de movies para obtener detalles de las películas
    movies_director = pd.merge(director_movies, movies, on='idMovies')
        
    if movies_director.empty:
        raise HTTPException(status_code=404, detail="No se encontraron películas dirigidas por el director especificado.")
        
    # Seleccionar columnas de interés
    result = movies_director[['title', 'release_date', 'return', 'budget', 'revenue']]
        
     # Calcular el éxito promedio del director
    avg_return = result['return'].mean()
        
    # Convertir DataFrame a diccionario para la respuesta
    movies_list = result.to_dict(orient='records')
        
    # Retornar la respuesta junto con el mensaje inicial
    return {
            'mensaje': f"Este endpoint devuelve las películas dirigidas por el director {nombre_director.title()} y su éxito promedio basado en el retorno de inversión.",
            'ejemplo_de_uso': f"Para buscar al director \"{nombre_director.title()}\", realiza una solicitud GET a /director/{nombre_director.title()}",
            'exito_promedio': avg_return,
            'peliculas': movies_list
        }

# Sistema de Recomendacion
@app.get("/recomendacion/")
async def recomendacion(titulo: str):
    """
    Busca recomendaciones de películas similares basadas en el título de la película proporcionada.

    Ejemplo de uso:
    - URL: /recomendacion/?titulo=Jumanji

    Parámetros:
    - `titulo`: Título de la película para la que se desean obtener recomendaciones (Ejemplo: "Jumanji").
    """

    # Verificar si el título está vacío o no es válido
    if not titulo:
        raise HTTPException(status_code=400, detail="Debe ingresar un título de película. Ejemplo: 'Jumanji'.")

    # Normalizar el título a minúsculas
    titulo_normalizado = titulo.lower()

    # Obtener las recomendaciones (considerando que la función de recomendación también normaliza los títulos)
    peliculas_recomendadas = recomendar_peliculas_por_similitud(titulo_normalizado)

    # Verificar si la película fue encontrada
    if not peliculas_recomendadas:
        raise HTTPException(status_code=404, detail="Película no encontrada. Asegúrese de ingresar el título correctamente, sin importar las mayúsculas o minúsculas. Ejemplo: 'Jumanji'.")

    return {"recomendaciones": peliculas_recomendadas}
