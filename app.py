from flask import Flask, render_template, redirect, url_for
import requests
from collections import namedtuple
import re


TMDB_URL = 'http://api.themoviedb.org/3/movie/popular'
TMDB_API_KEY = '9dbd6530be5d59e915f3630acc78409d'

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('movies'))


Movie = namedtuple('Movie', ['id', 'title', 'popularity', 'release_date'])

def movie_from_json(json_obj):
    return Movie(
        id = json_obj['id'],
        title = json_obj['title'],
        popularity = round(json_obj['popularity']),
        release_date = json_obj['release_date']
    )

@app.route('/movies/')
def movies():
    payload = {
        'api_key': TMDB_API_KEY,
        'sort_by': 'popularity.desc'
    }
    response = requests.get(TMDB_URL, data=payload)
    top_ten_movies = [ 
        movie_from_json(json_obj)
        for json_obj in
        response.json()['results'][:10]
    ]
    return render_template('movies.html', movies=top_ten_movies)

@app.route('/movies/<movie_id>')
def movie(movie_id):
    payload = {
        'api_key': TMDB_API_KEY
    }
    response = requests.get('http://api.themoviedb.org/3/movie/' + movie_id, data=payload)
    movie = movie_from_json(response.json())
    return render_template('movie.html', movie=movie)

if (__name__ == '__main__'):
    app.run(debug=True, use_reloader=False)