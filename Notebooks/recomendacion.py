import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_parquet('Dataset_procesados/movies_modificado.parquet')  # Cargar el archivo CSV

# Paso 1: Combinar los campos de 'género' y 'overview' en una columna de características
movies['combined_features'] = movies['genres'].str.lower() + " " + movies['overview'].str.lower()

# Paso 2: Vectorizar las características combinadas utilizando TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

# Paso 3: Función para recomendar películas
def recomendar_peliculas_por_similitud(titulo_pelicula, num_recomendaciones=5):
    # Convertir el título de la película a minúsculas para la búsqueda insensible a mayúsculas/minúsculas
    titulo_pelicula = titulo_pelicula.lower()

    # Obtener el índice de la película
    idx = movies[movies['title'].str.lower() == titulo_pelicula].index
    if idx.empty:
        return []

    idx = idx[0]

    # Calcular la similitud del coseno con todas las demás películas
    cosine_similarities = cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()

    # Ordenar las películas por puntuación de similitud (exceptuando la película misma)
    similar_indices = cosine_similarities.argsort()[-num_recomendaciones-1:-1][::-1]

    # Obtener los títulos de las películas con mayor puntuación de similitud
    similar_movies = movies.iloc[similar_indices]['title'].tolist()
    
    return similar_movies
