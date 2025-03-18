import repositories.swapi_repository as SWAPIRepository
from schemas.swapi_schema import FilmResponse


class SWAPIService:
    @staticmethod
    async def get_all_films() -> FilmResponse | None:
        return await SWAPIRepository.SWAPIRepository.get_all_films()