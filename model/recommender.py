import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import re
import os

class MovieRecommender:
    def __init__(self, movies_path, ratings_path=None):
        self.movies_df = pd.read_csv(movies_path)
        
        # Load ratings if provided
        if ratings_path:
            self.ratings_df = pd.read_csv(ratings_path)
            # Calculate average rating and vote count per movie
            ratings_agg = self.ratings_df.groupby('movieId').agg(
                vote_average=('rating', 'mean'),
                vote_count=('rating', 'count')
            ).reset_index()
            self.movies_df = self.movies_df.merge(ratings_agg, on='movieId', how='left')
            
            # Fill NaN values for movies with no ratings
            self.movies_df['vote_average'] = self.movies_df['vote_average'].fillna(0)
            self.movies_df['vote_count'] = self.movies_df['vote_count'].fillna(0)
            
            # Weighted Rating Calculation (IMDB formula)
            # WR = (v / (v+m)) * R + (m / (v+m)) * C
            C = self.movies_df['vote_average'].mean()
            m = self.movies_df['vote_count'].quantile(0.70) # 70th percentile
            
            def weighted_rating(x, m=m, C=C):
                v = x['vote_count']
                R = x['vote_average']
                return (v / (v+m) * R) + (m / (v+m) * C)
            
            self.movies_df['score'] = self.movies_df.apply(weighted_rating, axis=1)
        else:
             self.movies_df['score'] = 0

        # Extract Year from Title
        # Regex to find (YYYY) at the end of the title
        def extract_year(title):
            match = re.search(r'\((\d{4})\)', title)
            if match:
                return int(match.group(1))
            return 0
            
        self.movies_df['year'] = self.movies_df['title'].apply(extract_year)

        # Handle pipe-separated genres
        self.movies_df['genres'] = self.movies_df['genres'].fillna('')
        self.movies_df['genres_str'] = self.movies_df['genres'].str.replace('|', ' ')
        
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df['genres_str'])
        
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        
        self.movies_df = self.movies_df.reset_index()
        self.indices = pd.Series(self.movies_df.index, index=self.movies_df['title']).drop_duplicates()
        
        # Get unique genres for dropdown
        all_genres = set()
        for genres in self.movies_df['genres']:
            all_genres.update(genres.split('|'))
        self.all_genres = sorted(list(all_genres))
        if '(no genres listed)' in self.all_genres:
            self.all_genres.remove('(no genres listed)')


    def get_recommendations(self, title=None, genre=None, min_rating=0, min_year=1900, max_year=2030, num_recommendations=10):
        # Base candidates: All movies or similar movies
        if title and title in self.indices:
            idx = self.indices[title]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            # Take top 100 similar movies first, then apply filters
            # Doing this to ensure we recommend RELEVANT movies, not just any random movie that fits filters
            movie_indices = [i[0] for i in sim_scores[1:101]] 
            candidates = self.movies_df.iloc[movie_indices].copy()
        else:
            # If no specific movie given (or not found), we can recommend top rated movies overall that match filters
            # Or if title not found, we just look at top movies
             candidates = self.movies_df.copy()

        # Apply Filters
        if genre:
            candidates = candidates[candidates['genres'].str.contains(genre, case=False)]
        
        if min_rating:
            candidates = candidates[candidates['vote_average'] >= float(min_rating)]
            
        if min_year:
            candidates = candidates[candidates['year'] >= int(min_year)]
            
        if max_year:
            candidates = candidates[candidates['year'] <= int(max_year)]

        # Sort by Weighted Score (Quality)
        candidates = candidates.sort_values('score', ascending=False)
        
        # return top N
        return candidates.head(num_recommendations)[['title', 'genres', 'vote_average', 'year']].to_dict('records')
