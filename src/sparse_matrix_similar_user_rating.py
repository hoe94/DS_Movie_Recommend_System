import pandas as pd
from scipy.sparse import coo_matrix

'''
Stage 2: 

i. Concat the new_movie_df with input_df
ii. Add the index column on new_movie_df
iii. Create the Sparse Matrix from the new_movie_df
'''

def concatenate_input_df_movie_df(input_df, new_movie_df):
    concat_df = pd.concat([input_df, new_movie_df])
    return concat_df

def add_index_column(concat_df):
    concat_df['movie_id'] = concat_df['movie_id'].astype('str')
    concat_df['user_name_index'] = concat_df['user_name'].astype('category').cat.codes
    concat_df['movie_id_index'] = concat_df['movie_id'].astype('category').cat.codes
    return concat_df

def create_sparse_matrix(concat_df):
    movie_rating_coo = coo_matrix((concat_df["movie_rating"], (concat_df["user_name_index"], concat_df["movie_id_index"])))
    ratings_mat = movie_rating_coo.tocsr()
    return ratings_mat

def sparse_matrix_from_concat_df(concat_df):
    concat_df = add_index_column(concat_df)
    sparse_matrix = create_sparse_matrix(concat_df)
    return sparse_matrix