from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from containers import Container
from schemas.swapi_schema import FilmResponse
from services.swapi_service import SWAPIService

router = APIRouter(prefix="/api/swapi/films", tags=["swapi","films"])

@router.get("", response_model=FilmResponse)
@inject
async def films(swapi_service: SWAPIService = Depends(Provide[Container.swapi_service])):
    return await swapi_service.get_all_films()
