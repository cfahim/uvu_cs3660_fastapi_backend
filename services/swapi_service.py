import repositories.swapi_repository as SWAPIRepository


class SWAPIService:
    @staticmethod
    async def get_all_films():
        return await SWAPIRepository.SWAPIRepository.get_all_films()