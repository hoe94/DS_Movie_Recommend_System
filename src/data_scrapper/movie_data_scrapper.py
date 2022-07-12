import requests
import yaml
import json
import pandas as pd

with open('config.yaml', 'rb')as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_key = config['API_KEY']
dataset = pd.read_parquet('movie_dataset.parquet')
#dataset = pd.DataFrame(columns = ['adult','backdrop_path','genre_ids','id','original_language',\
#                        'original_title', 'popularity', 'poster_path', 'release_date', 'title', 'video', 'vote_average', 'vote_count'])

start_date = ['2022-01-01', '2022-04-01']
last_date = ['2022-03-31', '2022-06-09']

for input_start_date, input_last_date in zip(start_date, last_date):
#for input_year in range(2005, 2005+1):
    base_url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}'
    language = '&language=en-US'
    sort_by = '&sort_by=popularity.desc'
    #year = f'&primary_release_year={input_year}'
    gte = f"&primary_release_date.gte={input_start_date}"
    lte = f"&primary_release_date.lte={input_last_date}"

    #url = base_url + language + sort_by + year
    url = base_url + language + sort_by + gte + lte
    initial_response = requests.get(url).json()
    most_popular_films = initial_response["results"]

    #print(f'{input_year} data is ingesting into dataframe')
    print(f"\n{input_start_date}: {initial_response['total_pages']}")

    for page in range(2, initial_response["total_pages"]+1):
        print(f'Page Num: {page}')
        second_response = requests.get(url + f"&page={page}").json()
        most_popular_films.extend(second_response["results"])
     
    for i, movie_object in enumerate(most_popular_films):
        adult = movie_object['adult']
        backdrop_path = movie_object['backdrop_path']
        genre_ids = movie_object['genre_ids']
        id = movie_object['id']
        original_language = movie_object['original_language']
        original_title = movie_object['original_title']
        popularity = movie_object['popularity']
        poster_path = movie_object['poster_path']
        release_date = movie_object['release_date']
        title = movie_object['title']
        video = movie_object['video']
        vote_average = movie_object['vote_average']
        vote_count = movie_object['vote_count']

        dataset = dataset.append({'adult':adult, 'backdrop_path':backdrop_path,'genre_ids':genre_ids, 'id': id,
                                    'original_language': original_language, 'original_title': original_title, 'popularity': popularity,
                                    'poster_path': poster_path, 'release_date': release_date, 'title': title,
                                    'video':video,'vote_average': vote_average, 'vote_count': vote_count}, ignore_index = True)
    
dataset['genre_ids'] = dataset['genre_ids'].fillna('[]')
dataset['genre_ids'] = dataset['genre_ids'].astype(str)

print(dataset.shape)
print(max(dataset['release_date']))

dataset.to_parquet('movie_dataset.parquet')



