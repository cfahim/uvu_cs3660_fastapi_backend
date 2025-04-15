from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject

from containers import Container
from models.rbac_model import PermissionEnum
from schemas.swapi_schema import FilmResponse
from services.auth_service import AuthorizationService
from services.swapi_service import SWAPIService

router = APIRouter(prefix="/api/swapi/films", tags=["swapi","films"])

@router.get("", response_model=FilmResponse)
@inject
async def films(
    request: Request,
    swapi_service: SWAPIService = Depends(Provide[Container.swapi_service]),
    auth_service: AuthorizationService = Depends(Provide[Container.auth_service]),    
):
    auth_service.assert_permissions(request, [PermissionEnum.SWAPIREAD])
    try:
        return await swapi_service.get_all_films()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error from SWAPI: {e}")
