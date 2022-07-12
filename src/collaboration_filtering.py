import argparse
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from get_data_from_similar_users import get_data_from_similar_users
from sparse_matrix_similar_user_rating import concatenate_input_df_movie_df, sparse_matrix_from_concat_df
from get_top_N_neighbors import get_movies_from_top_N_neighbors
from get_top_N_movies import get_top_N_movies

'''Stage 0: Extract the movie_rating from user input'''
def extract_user_ratings(user_df):
    if 'movie_rating' not in user_df.columns:
        print("this input data doesn't exist the rating column")
    else:
        movie_id_list = [user_df.iloc[i,:]['movie_id'] for i in range(len(user_df))]
        return movie_id_list


'''Implementation part'''

def main(input_df, rating_df):
    #Stage 0: Extract the movie_rating from user input
    movie_list = extract_user_ratings(input_df)

    #Stage 1:
    new_movie_df = get_data_from_similar_users(rating_df, movie_list)

    #Stage 2:
    new_movie_df = concatenate_input_df_movie_df(input_df, new_movie_df)
    ratings_mat = sparse_matrix_from_concat_df(new_movie_df)

    #Stage 3:
    processed_movie_df = get_movies_from_top_N_neighbors(5, new_movie_df, ratings_mat)
    #Stage 4:
    filtered_movies_id = get_top_N_movies(processed_movie_df)

    #Retrieve the recommended movie id & movie_title pass to email function
    rating_df['movie_id'] = rating_df['movie_id'].astype('str')
    recommended_df = rating_df[rating_df['movie_id'].isin(filtered_movies_id)][['movie_id', 'movie_title']].reset_index(drop = True)
    recommended_df = recommended_df.drop_duplicates()

    recommended_dict = dict(recommended_df.values)
    return recommended_dict
    
    #filtered_movies_name = recommended_df['movie_title'].unique()
    #return filtered_movies_id, filtered_movies_name
  



if __name__ == "__main__":
    #movie_list = [558, 209112, 269149, 351819, 140300, 259694, 300671, 339984, 291870, 205584]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path",
        default = 'C:/Users/Hoe/Desktop/Learning/Python/Project 10 - Movie Recommendation/input_user_rating.parquet',
        help = "the location of the input data path"
    )
    args = parser.parse_args()

    rating_df = pd.read_parquet('movie_rating.parquet')
    input_df = pd.read_parquet(args.input_path)

    main(input_df, rating_df)


#new_movie_list.to_parquet('test.parquet')
#print({k: v for k, v in sorted(user_list.items(), key=lambda item: item[1])})
