import httpx


class SWAPIRepository:
    @staticmethod
    async def get_all_films():
        url = "https://swapi.dev/api/films/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            return None