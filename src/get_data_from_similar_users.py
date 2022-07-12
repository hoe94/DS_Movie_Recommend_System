import pandas as pd

'''
Stage 1: 

i) Get the users who have rated the movie I like
ii) Get the movies they rated from the similar users
'''
def get_similar_users(rating_df, input_list):
    similar_user_list = {}
    input_list = set(list(dict.fromkeys(input_list)))

    for i in range(len(rating_df)):
        movie_id = rating_df.iloc[i,:]['movie_id']
        user_name = rating_df.iloc[i,:]['user_name']

        if movie_id in input_list:
            if user_name not in similar_user_list:
                similar_user_list[user_name] = 1
            else:
                similar_user_list[user_name] +=1
        else:
            pass
        
    return similar_user_list

def get_movies_from_similar_users(rating_df, user_list, input_movie_list):
    user_list = list(dict.fromkeys(user_list))
    #new_movie_list = []
    new_movie_list = pd.DataFrame(columns = ['user_name', 'movie_id', 'movie_title', 'movie_rating'])

    for user in user_list:
        user_df = rating_df[rating_df['user_name'] == user]
        for index, row in user_df.iterrows():
            movie_id = row['movie_id']
            movie_title = row['movie_title']
            movie_rating = row['rating']

            if movie_id not in input_movie_list:
                new_movie_list = new_movie_list.append({'user_name': user, 'movie_id': movie_id, 'movie_title': movie_title, 'movie_rating': movie_rating}, ignore_index= True)
            else:
                pass
    new_movie_list = new_movie_list.drop_duplicates()
    return new_movie_list

def get_data_from_similar_users(rating_df, movie_list):
    user_list = get_similar_users(rating_df, movie_list)
    new_movie_df = get_movies_from_similar_users(rating_df, user_list, movie_list)
    return new_movie_df