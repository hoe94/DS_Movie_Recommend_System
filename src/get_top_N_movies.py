import pandas as pd
import numpy as np

'''
Stage 4:
iii. Apply Ranking method to filter the movies
'''

def get_top_N_movies(agg_df):
    #agg_df = agg_df[agg_df['score'] > 1.0]
    agg_df = agg_df.head()
    filtered_movies_list = [agg_df.iloc[i,:]['movie_id'] for i in range(len(agg_df))]
    return filtered_movies_list