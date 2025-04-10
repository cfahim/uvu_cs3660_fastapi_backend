import repositories.swapi_repository as SWAPIRepository
from schemas.swapi_schema import FilmResponse


class SWAPIService:
    def __init__(self, swapi_repository: SWAPIRepository.SWAPIRepository): 
        self.swapi_repository = swapi_repository

    
    async def get_all_films(self) -> FilmResponse | None:
        return await self.swapi_repository.get_all_films()