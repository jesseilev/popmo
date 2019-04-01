from flask import Flask, render_template, redirect, url_for
import requests
from collections import namedtuple
import re



##### MOVIE DATA MODEL #####

Movie = namedtuple(
    'Movie', 
    ['id', 'title', 'popularity', 'release_date']
)

def movie_from_json(json_obj):
    return Movie(
        id = json_obj['id'],
        title = json_obj['title'],
        popularity = round(json_obj['popularity']),
        release_date = json_obj['release_date']
    )



##### TMDB API #####

TMDB_URL = 'http://api.themoviedb.org/3/movie/'
TMDB_API_KEY = '9dbd6530be5d59e915f3630acc78409d'

def fetch_popular_movies():
    url = TMDB_URL + 'popular'
    payload = {
        'api_key': TMDB_API_KEY,
        'sort_by': 'popularity.desc'
    }
    response = requests.get(url, data=payload)
    top_ten_movies = [ 
        movie_from_json(json_obj)
        for json_obj in
        response.json()['results'][:10]
    ]
    return top_ten_movies

def fetch_movie(movie_id):
    url = TMDB_URL + movie_id
    payload = {
        'api_key': TMDB_API_KEY
    }
    response = requests.get(url, data=payload)
    movie = movie_from_json(response.json())
    return movie


##### APP ######

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('movies'))

@app.route('/movies/')
def movies():
    movies = fetch_popular_movies()
    return render_template('movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def movie(movie_id):
    movie = fetch_movie(movie_id)
    return render_template('movie.html', movie=movie)

if (__name__ == '__main__'):
    app.run(debug=True, use_reloader=False)