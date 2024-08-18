from fastapi import FastAPI
import pandas as pd
from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any

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
@app.get("/cantidad_filmaciones_mes/{mes}")
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
        return "Mes no válido."

# 2. Función para cantidad de filmaciones por día
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias = {
        "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "domingo": 6
    }
    dia_num = dias.get(dia.lower())
    if dia_num is not None:
        cantidad = movies[movies['fecha_lanzamiento'].dt.weekday == dia_num].shape[0]
        return f"{cantidad} películas fueron estrenadas en los días {dia.capitalize()}."
    else:
        return "Día no válido."

# 3. Función para obtener el score por título
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    film = movies[movies['title'].str.lower() == titulo.lower()]
    if not film.empty:
        titulo = film.iloc[0]['title']
        año = film.iloc[0]['release_year']
        score = film.iloc[0]['popularity']
        return f"La película {titulo} fue estrenada en el año {año} con un score/popularidad de {score}."
    else:
        return "Película no encontrada."

# 4. Función para obtener los votos por título
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
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

# 5. Función para obtener informacion sobre el actor
@app.get("/actor/{nombre_actor}")
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
    nombre_actor = nombre_actor.casefold()  # o nombre_actor.lower()

    # Filtrar el dataset cast por el nombre del actor (también insensible a mayúsculas)
    actor_films = cast_df[cast_df['name_actor'].str.casefold() == nombre_actor]
    
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

# 6. Función para obtener información sobre un director
@app.get("/get_director")
def get_director(nombre_director: str) -> Dict[str, Any]:
    """
    Busca información sobre el éxito de las películas dirigidas por el director proporcionado.

    Ejemplo de uso:
    - URL: /get_director?nombre_director=Steven%20Spielberg
    
    Parámetros:
    - `nombre_director`: Nombre del director (Ejemplo: "Steven Spielberg")

    Retorna:
    - Mensaje descriptivo.
    - Éxito promedio basado en el retorno de inversión.
    - Lista de películas con detalles como el título, fecha de lanzamiento, retorno, costo y ganancia.

    Ejemplo de Respuesta:
    {
        "mensaje": "Este endpoint devuelve las películas dirigidas por el director especificado y su éxito promedio basado en el retorno de inversión.",
        "ejemplo_de_uso": "Para buscar al director 'Steven Spielberg', realiza una solicitud GET a /get_director con el parámetro nombre_director=Steven%20Spielberg",
        "nombre_director": "Steven Spielberg",
        "exito_promedio": 0.45,
        "peliculas": [
            {
                "title": "Jurassic Park",
                "release_date": "1993-06-11",
                "return": 0.78,
                "budget": 63000000,
                "revenue": 1070000000
            },
            ...
        ]
    """
    try:
        # Filtrar el dataset de crew para obtener las películas del director especificado
        director_movies = crew_df[
            (crew_df['crew_name'] == nombre_director) & 
            (crew_df['crew_job'] == 'Director')
        ]
        
        if director_movies.empty:
            raise HTTPException(status_code=404, detail="Director no encontrado. Asegúrate de que el nombre esté escrito correctamente y que el director haya dirigido al menos una película en la base de datos.")
        
        # Unir con el dataset de movies para obtener detalles de las películas
        movies_director = pd.merge(director_movies, movies, on='idMovies')
        
        # Verificar si hay datos después de la unión
        if movies_director.empty:
            raise HTTPException(status_code=404, detail="No se encontraron películas dirigidas por el director especificado.")
        
        # Seleccionar columnas de interés
        result = movies_director[['title', 'release_date', 'return', 'budget', 'revenue']]
        
        # Calcular el éxito promedio del director
        avg_return = result['return'].mean()
        
        # Convertir DataFrame a diccionario para la respuesta
        movies_list = result.to_dict(orient='records')
        
        return {
            'mensaje': 'Este endpoint devuelve las películas dirigidas por el director especificado y su éxito promedio basado en el retorno de inversión.',
            'ejemplo_de_uso': 'Para buscar al director "Steven Spielberg", realiza una solicitud GET a /get_director con el parámetro nombre_director=Steven%20Spielberg',
            'nombre_director': nombre_director,
            'exito_promedio': avg_return,
            'peliculas': movies_list
        }
    except Exception as e:
        # Captura cualquier excepción inesperada
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    

#Funcion para el  Sistema de recomendación de Peliculas
def recomendar_peliculas(titulo_pelicula, num_recomendaciones=5):
    # Obtener el índice de la película
    idx = movies[movies['title'] == titulo_pelicula].index
    if idx.empty:
        return []

    idx = idx[0]

    # Calcular la similitud con todas las demás películas
    cosine_similarities = cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()

    # Obtener los índices de las películas más similares
    similar_indices = cosine_similarities.argsort()[-num_recomendaciones-1:-1]

    # Obtener los nombres de las películas más similares
    similar_movies = movies.iloc[similar_indices]['title'].tolist()
    return similar_movies

@app.get("/recomendacion/")
async def recomendacion(titulo: str):
    # Obtener las recomendaciones
    peliculas_recomendadas = recomendar_peliculas(titulo)

    # Verificar si la película fue encontrada
    if not peliculas_recomendadas:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    return {"recomendaciones": peliculas_recomendadas}
