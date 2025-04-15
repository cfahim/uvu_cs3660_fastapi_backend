import httpx

from schemas.swapi_schema import FilmResponse


class SWAPIRepository:
    def __init__(self): 
        self.base_url = "https://swapi.dev/api"

    async def get_all_films(self) -> FilmResponse | None:
        url = f"{self.base_url}/films"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return FilmResponse(**response.json())
        return None