from flask import Flask, render_template, request
import pandas as pd
from model.recommender import MovieRecommender
import os

app = Flask(__name__)

# Initialize recommender
# We use a global variable to load it once at startup
recommender = None

def get_recommender():
    global recommender
    if recommender is None:
        movies_path = os.path.join(os.path.dirname(__file__), 'movies.csv')
        ratings_path = os.path.join(os.path.dirname(__file__), 'ratings.csv')
        recommender = MovieRecommender(movies_path, ratings_path)
    return recommender

@app.route('/')
def index():
    rec_engine = get_recommender()
    return render_template('index.html', genres=rec_engine.all_genres)

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form.get('movie_name')
    genre = request.form.get('genre')
    rating = request.form.get('rating')
    min_year = request.form.get('min_year')
    max_year = request.form.get('max_year')
    
    rec_engine = get_recommender()
    
    # Handle empty strings/defaults
    kwargs = {}
    if title: kwargs['title'] = title
    if genre and genre != 'All': kwargs['genre'] = genre
    if rating: kwargs['min_rating'] = rating
    if min_year: kwargs['min_year'] = min_year
    if max_year: kwargs['max_year'] = max_year
    
    recommendations = rec_engine.get_recommendations(**kwargs)
    
    # If no results found
    if not recommendations:
         return render_template('index.html', error="No movies found matching your criteria.", movie_name=title, genres=rec_engine.all_genres)

    return render_template('index.html', recommendations=recommendations, movie_name=title, genres=rec_engine.all_genres)

if __name__ == '__main__':
    app.run(debug=True)
