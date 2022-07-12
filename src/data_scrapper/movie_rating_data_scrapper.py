import requests
import yaml
import json
import pandas as pd

with open('config.yaml', 'rb')as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_key = config['API_KEY']
df = pd.read_parquet('movie_dataset.parquet')
not_available_movie_list = pd.read_parquet('not_available_movie_list.parquet')
#not_available_movie_list = pd.DataFrame(columns = ['no', 'movie_id', 'movie_title'])
movies_rating = pd.read_parquet('movie_rating.parquet')

#1. Data Preprocessing on movies dataset
df['release_year'] = df['release_date'].str[0:4].astype(int)
def filter_date_df(start_year, end_year):
    filtered_df = df[ (df['release_year'] >= start_year) & (df['release_year'] <= end_year)]
    return filtered_df
df = filter_date_df(2021, 2022) #2021 - 2022
print(df.shape)

for i in range(len(df)):
    movie_id = df.iloc[i, :]['id']
    movie_title = df.iloc[i,:]['title']
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}&language=en-US'
    try:
        response = requests.get(url).json()
        results = response['results']
        for inner_results in results:
            user_name = inner_results['author_details']['username']
            rating = inner_results['author_details']['rating']
            print(i, movie_id, movie_title, user_name, rating)
            movies_rating = movies_rating.append({'no': i, 'movie_id': movie_id, 'movie_title': movie_title, 'user_name': user_name, 'rating': rating}, ignore_index = True)
    except:
        not_available_movie_list = not_available_movie_list.append({'no': i, 'movie_id': movie_id, 'movie_title': movie_title}, ignore_index= True)

not_available_movie_list.to_parquet('not_available_movie_list.parquet')
movies_rating.to_parquet('movie_rating.parquet')