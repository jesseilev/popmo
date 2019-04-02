from flask import Flask, render_template, redirect, url_for
import requests
from collections import namedtuple




############################
##### MOVIE DATA MODEL #####
############################


# Movie
#
# a namedtuple representing a TMDB movie resource
Movie = namedtuple(
    'Movie', 
    [
        'id', # the tmdb ID for the movie
        'title', # the name of the movie
        'popularity', # the movie's TMDB popularity score
        'release_date', # the date the movie came out in theaters
        'poster_url' # url for the movie poster image
    ]
)

# movie_from_json
#
# converts a json object into a Movie tuple
def movie_from_json(json_obj):
    return Movie(
        id = json_obj['id'],
        title = json_obj['title'],
        popularity = round(json_obj['popularity']),
        release_date = json_obj['release_date'],
        poster_url = TMDB_IMAGE_URL + json_obj['poster_path']
    )




####################
##### TMDB API #####
####################


TMDB_BASE_URL = 'http://api.themoviedb.org/3/movie'
TMDB_IMAGE_URL = 'http://image.tmdb.org/t/p/w200'
TMDB_API_KEY = '9dbd6530be5d59e915f3630acc78409d'


# fetch_popular_movies
#
# fetches the latest data from the tmdb 'popular movies' endpoint
# if the request was sucessful, returns a list of Movie tuples
# if the request failed, returns None
def fetch_popular_movies():

    # prep the arguments to make a GET request
    url = TMDB_BASE_URL + '/popular'
    payload = {
        'api_key': TMDB_API_KEY,
        'sort_by': 'popularity.desc'
    }

    # make the request and cache the response
    response = requests.get(url, data=payload)

    # check that the request was sucessful
    if (response.status_code == 200):

        # convert to json and extract the 'results' array from the json object
        results = response.json()['results']
        
        # take the first 10 items from the results array and map each json object to a Movie tuple
        top_ten_movies = [ 
            movie_from_json(json_obj) for json_obj in results[:10]
        ]

        # return the movies
        return top_ten_movies


# fetch_movie
#
# fetches details for the movie with id `movie_id` from TMDB api
# if the request was sucessful, returns a Movie tuple
# if the request failed, returns None
def fetch_movie(movie_id):
    # prep the arguments to make the request
    url = TMDB_BASE_URL + '/' + movie_id
    payload = {
        'api_key': TMDB_API_KEY
    }

    # make the request and caceh the response
    response = requests.get(url, data=payload)

    # if the request was successful
    if (response.status_code == 200):

        # map the json into a Movie and return the movie
        movie = movie_from_json(response.json())
        return movie



################
##### APP ######
################

app = Flask(__name__)


# the home route redirects to /movies/
@app.route('/')
def index():
    return redirect(url_for('movies'))


# route for viewing today's most popular movies
@app.route('/movies/')
def movies():
    # attempt to fetch today's popular movies
    movies = fetch_popular_movies()

    if movies:
        # if successful, render the movies.html template
        return render_template('movies.html', movies=movies)
    else:
        # otherwise render an error message
        return render_template('error.html', 
            message = "Something went wrong when I tried to lookup today's movies. Sorry!" 
        )


# route for viewing details about a particular movie
@app.route('/movies/<movie_id>')
def movie(movie_id):
    # attempt to fetch the movie with the id from the url
    movie = fetch_movie(movie_id)
    if movie:
        # if successful, render the movie.html template
        return render_template('movie.html', movie=movie)
    else:
        # otherwise render an error message
        return render_template('error.html', 
            message = "Something went wrong when I tried to look up this movie. Sorry!"
        )
