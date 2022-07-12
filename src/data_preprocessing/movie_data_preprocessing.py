import pandas as pd

movie_df = pd.read_parquet('movie_dataset.parquet')

#1. Create new column, release_year based on release_date
movie_df['release_year'] = movie_df['release_date'].str[0:4].astype(int)
movie_df = movie_df[['adult' ,'backdrop_path', 'genre_ids', 'id',
                    'original_language', 'original_title', 'popularity',
                    'poster_path', 'release_date', 'release_year', 'title',
                    'video','vote_average', 'vote_count']]


movie_df.to_parquet('movie_dataset.parquet', index = False)