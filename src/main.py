from modules.data_loader import DataLoader
from modules.birch_model import BirchModel
from modules.recommender import RecommendationSystem

from models.data_loader_config import DataLoaderConfig
from models.dto import NewRatings

from utils.logger import BasicLogger
from utils.validator import Validator
from utils.converter import Converter

import pandas as pd
import time

# initialize the logger
logger = BasicLogger('debug')

# set the dataloader config
dataloader_config = DataLoaderConfig(
    users_path='data/users.dat',
    ratings_path='data/ratings.dat',
    movies_path='data/movies.dat',
    seperator='::',

    user_columns= ['user_id', 'gender', 'age', 'occupation', 'zip'],
    rating_columns= ['user_id', 'movie_id', 'rating', 'timestamp'],
    movie_columns= ['movie_id', 'title', 'genres']
)

# create the dataloader
dataloader = DataLoader(dataloader_config, logger)

# load the data
dataloader.load_data()

# preprocess the data
dataloader.preprocess_data()

# create the clustering model
clustering_model = BirchModel(dataloader.user_features, logger)

# train the model
clustering_model.train(18, batch_size=10)

# initialize the recommendation system
rs = RecommendationSystem(dataloader, clustering_model, logger)

# run the simulation
logger.log_info('Starting the simulation')

# get the inputs
gender = input('Enter your gender (M/F): ')
age = input('Enter your age: ')

# create the new user
new_user = {
    'user_id': int(dataloader.user_data['user_id'].max() + 1),
    'gender': Converter.gender_to_category(gender),
    'age': Converter.age_to_category(age)
}


new_user_features = {
    "user_id":      new_user['user_id'],
    "Action":       0.00,
    "Adventure":    0.00,
    "Animation":    0.00,
    "Children's":   0.00,
    "Comedy":       50.00,
    "Crime":        0.00,
    "Documentary":  0.00,
    "Drama":        0.00,
    "Fantasy":      0.00,
    "Film-Noir":    0.00,
    "Horror":       0.00,
    "Musical":      0.00,
    "Mystery":      0.00,
    "Romance":      50.00,
    "Sci-Fi":       0.00,
    "Thriller":     0.00,
    "War":          0.00,
    "Western":      0.00,
    "gender":       new_user['gender'],
    "age":          new_user['age']   
}

logger.log_debug(f'Creating new user with user_id: {new_user["user_id"]}', age=new_user['age'], gender=new_user['gender'])

ACTIVE_USER = new_user['user_id']

new_user_features = pd.DataFrame(new_user_features, index=[0])

dataloader.add_user(new_user)
clustering_model.update(new_user_features)

run = True
while run:
    # get recommendations
    recommendations = rs.get_topk_recommendations(ACTIVE_USER, 5)

    new_ratings = []

    for _, recommendation in recommendations.iterrows():
        query = input(f"How would you rate {recommendation['title']} [{recommendation['genres']}]? : ")

        if query == 'q':
            logger.log_info('Exiting the simulation')
            run = False
            break

        # validate the rating
        if not Validator.is_valid_rating(query):
            logger.log_error('Invalid rating. Please enter a number between 0 and 5', ValueError("Invalid rating"))
            continue

        new_ratings.append(NewRatings(
            user_id     = ACTIVE_USER,
            movie_id    = recommendation['movie_id'],
            rating      = int(query),
            timestamp   = int(time.time())
        ))

    new_ratings = pd.DataFrame(new_ratings)
    rs.update_ratings(ACTIVE_USER, new_ratings)
    pd.DataFrame(new_ratings).to_csv('data/new_ratings.csv', index=False, mode='a', header=False)

logger.log_info('Simulation completed')