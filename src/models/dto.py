from dataclasses import dataclass


@dataclass
class NewRatings:
    user_id: int
    movie_id: int
    rating: float
    timestamp: int