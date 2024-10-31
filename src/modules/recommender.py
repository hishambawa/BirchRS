import pandas as pd
from modules.data_loader import DataLoader
from utils.logger import BasicLogger
from interfaces.clustering import IClusteringModel

class RecommendationSystem:

    def __init__(self, dataloader: DataLoader, clustering_model: IClusteringModel, logger: BasicLogger):
        self.logger = logger
        self.clustering_model = clustering_model
        self.dataloader = dataloader

    def get_topk_recommendations(self, user_id, k=5, min_rating=4):
        # get the similar users
        similar_users = self.clustering_model.get_similar_users(user_id)

        # get the list of items the active user has already rated
        rated_items = self.dataloader.rating_data[self.dataloader.rating_data['user_id'] == user_id]['movie_id']

        # get the items rated highly by the similar users
        # but not rated by the active user
        liked_items_in_group = self.dataloader.rating_data[ (self.dataloader.rating_data['user_id'].isin(similar_users)) &
                                                    (self.dataloader.rating_data['rating'] >= min_rating) &
                                                    (~self.dataloader.rating_data['movie_id'].isin(rated_items))]
        
        # get the number of times the items were rated by the users
        aggregation = liked_items_in_group.groupby('movie_id').size().reset_index(name='count').sort_values('count', ascending=False)

        # append the title of the item
        aggregation = pd.merge(aggregation, self.dataloader.movie_data[['movie_id', 'title', 'genres']], on='movie_id')

        # return topK items
        return aggregation[['title', 'movie_id', 'genres']].head(k)
    
    def update_ratings(self, user_id, new_data: pd.DataFrame):
        # check if there are any ratings to update
        if len(new_data) == 0:
            self.logger.log_info('No new ratings to update')
            return

        self.logger.log_info('Updating ratings')
        # update the ratings in the data loader
        new_ratings = self.dataloader.append_new_ratings(user_id, new_data)

        # get the clustering features of the new data
        new_features = self.dataloader.get_clustering_features(new_ratings)

        # update the clustering model
        self.clustering_model.update(new_features)
        self.logger.log_info('Data updated successfully')

    # helper method to fetch and print the recommendations
    def print_recommendations(self, user_id, k=5):
        recommendations = self.get_topk_recommendations(user_id, k)

        self.logger.log_info(f'Top 5 recommendations for user {user_id}')
        for idx, recommendation in recommendations.iterrows():
            self.logger.log_info(f'{idx}. {recommendation["title"]} [{recommendation["genres"]}]')