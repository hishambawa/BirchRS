from dataclasses import dataclass

@dataclass
class DataLoaderConfig:
    users_path: str
    ratings_path: str
    movies_path: str
    seperator: str

    user_columns: list
    rating_columns: list
    movie_columns: list