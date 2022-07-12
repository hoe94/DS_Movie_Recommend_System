import pandas as pd

rating_df = pd.read_parquet('movie_rating.parquet')

#1. check the the duplicate rows in movie_rating df
duplicated_df = rating_df[rating_df.duplicated(keep = False)]
print(f"There are {len(duplicated_df['movie_title'].unique())} movies have the duplicated ratings")

#2. drop the duplicated rows
rating_df.drop_duplicates(inplace = True)

#3. fill the nan value on column, rating into 0
rating_df['rating'] = rating_df['rating'].fillna(0)

rating_df.to_parquet('movie_rating.parquet')