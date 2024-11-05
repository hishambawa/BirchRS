from abc import ABC, abstractmethod
import pandas as pd

class IClusteringModel(ABC):
    @abstractmethod
    def train(self, n_clusters: int, batch_size = 100):
        pass

    @abstractmethod
    def update(self, new_data: pd.DataFrame):
        pass

    @abstractmethod
    def get_cluster(self, user_id: int):
       pass
    
    @abstractmethod
    def get_similar_users(self, user_id: int):
       pass