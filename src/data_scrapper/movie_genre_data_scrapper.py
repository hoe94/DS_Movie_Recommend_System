import requests
import yaml
import json
import pandas as pd

with open('config.yaml', 'rb')as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_key = config['API_KEY']
genre_list = pd.DataFrame(columns = ['id', 'name'])

url = f'https://api.themoviedb.org/3/genre/movie/list?language=en-US&api_key={api_key}'
response = requests.get(url).json()

genre_json = response['genres']
for object in genre_json:
    id = object['id']
    name = object['name']

    genre_list = genre_list.append({'id': id, 'name': name}, ignore_index = True)

genre_list['id'] = genre_list['id'].astype(int)
genre_list = genre_list.sort_values(by = ['id'], ascending = True)
genre_list.to_parquet('movie_genre.parquet', index = False)
