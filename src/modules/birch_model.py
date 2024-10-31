from sklearn.cluster import Birch

from utils.logger import BasicLogger

from interfaces.clustering import IClusteringModel

import pandas as pd

class BirchModel(IClusteringModel):
    def __init__(self, data: pd.DataFrame, logger: BasicLogger):
        self.logger = logger

        self.data = data
        self.model = None
        self.clusters = None

    def train(self, n_clusters: int, batch_size: int):
        self.logger.log_info('Training the clustering model')

        # initialize the clustering model
        self.model = Birch(n_clusters=None, threshold=0.01)

        # prepare the data to train the model
        features = self.data.drop(columns=['user_id'])

        #train the model in batches
        for start in range(0, len(features), batch_size):
            end = start + batch_size
            print(f'Fitting the model with data from {start} to {end}', end='\r')
            self.model.partial_fit(features[start:end])

        # once the model is trained, set the number of clusters
        # and re-train to get global clusters
        self.model.set_params(n_clusters=n_clusters)
        self.model.partial_fit()

        # get the cluster labels
        self.data['cluster'] = self.model.predict(features)

        self.logger.log_info('Clustering model trained successfully')

    def update(self, new_data: pd.DataFrame):
        # prepare the data to re-train the model
        features = new_data.drop(columns=['user_id'])

        # partially train the model with new data
        self.model.partial_fit(features)

        # update the clusters
        new_data['cluster'] = self.model.predict(features)

        # check if the user already exists in the data
        # if not, append the new data
        if self.data['user_id'].isin(new_data['user_id']).any():
            self.logger.log_info('User already exists in the cluster. Updating the user')
            
            # replace the old datapoints with the new data
            self.data[self.data['user_id'].isin(new_data['user_id'])] = new_data

        else:
            self.logger.log_info('User does not exist in the cluster. Adding the user')
            self.data = pd.concat([self.data, new_data])

        self.logger.log_info('Clustering model updated successfully')

    def get_cluster(self, user_id: int):
        # get the cluster for the given user
        user_cluster = self.data.loc[self.data['user_id'] == user_id, 'cluster'].values[0]

        return user_cluster
    
    def get_similar_users(self, user_id: int):
        # get the cluster for the given user
        user_cluster = self.get_cluster(user_id)

        # get all users in the same cluster
        similar_users = self.data[self.data['cluster'] == user_cluster]

        return similar_users['user_id'].values