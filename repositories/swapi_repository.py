import httpx

from schemas.swapi_schema import FilmResponse


class SWAPIRepository:
    @staticmethod
    async def get_all_films() -> FilmResponse | None:
        url = "https://swapi.dev/api/films/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return FilmResponse(**response.json())
        return None