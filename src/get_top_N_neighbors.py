import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

'''
Stage 3:
i. Find the top N neighbors from input user based on cosine similarity (N: 5)
ii. Create new column, count & mean for movies to calculate the scoring method
iii. Apply Ranking method to filter the movies
'''
def get_movies_from_top_N_neighbors(n_neighbors, new_movie_df, rating_matrix):
    
    input_index = 7
    n_neighbors = -(n_neighbors)
    similarity = cosine_similarity(rating_matrix[input_index, :], rating_matrix).flatten()
    indices = np.argpartition(similarity, n_neighbors)[n_neighbors:]
    
    filtered_df = new_movie_df[new_movie_df['user_name_index'].isin(indices)]
    filtered_df = filtered_df[filtered_df['user_name_index'] != 7]

    #Scoring method
    agg_df = filtered_df.groupby('movie_id').movie_rating.agg(['count','mean'])
    agg_df = agg_df.reset_index()
    
    agg_df['adjusted_count'] = agg_df['count'] * (agg_df['count'] / agg_df['mean'])
    agg_df['score'] = agg_df['mean'] * agg_df['adjusted_count']
    agg_df = agg_df.sort_values(by = 'count', ascending = False)
    return agg_df