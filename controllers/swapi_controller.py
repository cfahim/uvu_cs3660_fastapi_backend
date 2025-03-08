from fastapi import APIRouter

from services.swapi_service import SWAPIService

router = APIRouter(prefix="/api/swapi/films", tags=["swapi","films"])

@router.get("/")
async def films():
    return await SWAPIService.get_all_films()
    