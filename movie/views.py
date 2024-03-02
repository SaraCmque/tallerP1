from django.shortcuts import render
from django.http import HttpResponse
from movie.models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from collections import Counter

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}
    genre_counter = Counter()

    # Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
    
    for movie in all_movies:
        genres = movie.genre.split(', ')  # Esto crea una lista de géneros para la película
        genre_counter.update(genres)  # Actualiza el contador con la lista de géneros

    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center', color='skyblue')
    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    
    genres = list(genre_counter.keys())
    counts = list(genre_counter.values())

    # Crear la gráfica de barras para géneros
    plt.figure(figsize=(10, 5))  # Ajusta el tamaño según sea necesario
    plt.bar(genres, counts, color='skyblue')
    plt.title('Movies by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(rotation=90)  # Rota los nombres de los géneros para mejor lectura
    plt.tight_layout()  # Ajusta automáticamente los parámetros de la subtrama

    # Guardar la gráfica en un objeto BytesIO y convertirla a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    graphic_genre = base64.b64encode(buffer.getvalue())
    graphic_genre = graphic_genre.decode('utf-8')
    buffer.close()

    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic_genre': graphic_genre,'graphic': graphic})


def home(request):
    # return HttpResponse('<h1>Welcome to Home Page! :D</h1>')
    # return render(request, 'home.html', {'name':'Sara Cortes'})
    searchTerm  = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})
    # return HttpResponse('<h1>Welcome to Home Page! :D</h1>')

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

