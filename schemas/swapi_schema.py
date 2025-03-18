from typing import List, Union
from pydantic import BaseModel

class Film(BaseModel):
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: str
    characters: List[str]
    planets: List[str]
    starships: List[str]
    vehicles: List[str]
    species: List[str]
    created: str
    edited: str
    url: str


class FilmResponse(BaseModel):
    count: int
    next: Union[str,None] = None
    previous: str|None = None
    results: List[Film]
