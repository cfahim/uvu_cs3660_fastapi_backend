from fastapi import APIRouter

from schemas.swapi_schema import FilmResponse
from services.swapi_service import SWAPIService

router = APIRouter(prefix="/api/swapi/films", tags=["swapi","films"])

@router.get("/", response_model=FilmResponse)
async def films():
    return await SWAPIService.get_all_films()
    