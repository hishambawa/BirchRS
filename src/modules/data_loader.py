import pandas as pd

from models.data_loader_config import DataLoaderConfig
from utils.logger import BasicLogger

class DataLoader:
    def __init__(self, config: DataLoaderConfig, logger: BasicLogger):
        self.config = config
        self.logger = logger

        self.user_data = None
        self.rating_data = None
        self.movie_data = None

        # used by the clustering model
        self.user_features = None
        self.df_percentage = None

    def load_data(self):
        self.logger.log_info('Loading data')

        self.user_data = pd.read_csv(self.config.users_path, sep=self.config.seperator, engine='python', names=self.config.user_columns)
        self.rating_data = pd.read_csv(self.config.ratings_path, sep=self.config.seperator, engine='python', names=self.config.rating_columns)
        self.movie_data = pd.read_csv(self.config.movies_path, sep=self.config.seperator, engine='python', names=self.config.movie_columns)

        self.logger.log_info('Data loaded successfully')

    def preprocess_data(self):
        self.logger.log_info('Preprocessing data')

        # remove the unused columns
        self.user_data.drop(columns=['zip'], inplace=True)
        self.user_data.drop(columns=['occupation'], inplace=True)

        # one-hot encode gender for demographic data
        # 0 if male and 1 if female
        self.user_data['gender'] = self.user_data['gender'].map({'M': 0, 'F': 1})

        # process genres for movies
        self.movie_data = pd.concat([self.movie_data, self.movie_data['genres'].str.get_dummies('|')], axis=1)
        
        # merge ratings with movie and user data
        self.rating_data = self.rating_data.merge(self.movie_data, on='movie_id')

        # get the clustering features
        self.user_features = self.get_clustering_features(self.rating_data)

        self.logger.log_info('Data preprocessed successfully')

    def get_clustering_features(self, rating_data):
        # filter ratings for high ratings (>4) and find the most liked categories per user
        # high_ratings = rating_data[rating_data['rating'] > 4]
        # liked_genres = high_ratings.groupby('user_id').sum(numeric_only=True)
        liked_genres = rating_data.groupby('user_id').sum(numeric_only=True)
        
        # merge the genres with user demographics
        # drop the unnecessary columns
        user_features = liked_genres.merge(self.user_data[['user_id', 'gender', 'age']], on='user_id')
        user_features.drop(columns=['movie_id', 'rating', 'timestamp'], inplace=True)
        
        genres = [
            "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
            "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
            "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
        ]

        # calculate how much a user likes each genre as a percentage
        # eg: if a user rated one item only with genres Action and Adventure, 
        # the percentage of Action and Adventure will be 50% each
        user_features[genres] = user_features[genres].apply(lambda x: 100 * x / x.sum(), axis=1).round(2)

        return user_features
    
    def append_new_ratings(self, user_id, new_ratings):
        # process the data
        new_ratings = pd.DataFrame(new_ratings)

        # get the ratings for the user
        user_ratings = self.rating_data[self.rating_data['user_id'] == user_id]

        # add the movie data to the new ratings
        new_ratings = pd.merge(new_ratings, self.movie_data, on='movie_id')

        # append the new ratings to the existing user ratings
        processed_ratings = pd.concat([user_ratings, new_ratings])

        # update the global ratings with the new data
        self.rating_data = pd.concat([self.rating_data, new_ratings])

        self.logger.log_debug('Ratings updated successfully')

        return processed_ratings
    
    def add_user(self, user_data):
        # add the new user to the user data
        self.user_data = pd.concat([self.user_data, pd.DataFrame([user_data])])

        self.logger.log_info('User added successfully')